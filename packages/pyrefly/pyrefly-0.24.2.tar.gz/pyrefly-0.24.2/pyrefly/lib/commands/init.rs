/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use std::io::Write;
use std::path::Path;
use std::path::PathBuf;

use anyhow::Context as _;
use clap::Parser;
use parse_display::Display;
use path_absolutize::Absolutize;
use pyrefly_util::display;
use pyrefly_util::fs_anyhow;
use tracing::error;
use tracing::info;
use tracing::warn;

use crate::commands::check;
use crate::commands::config_migration;
use crate::commands::config_migration::write_pyproject;
use crate::commands::globs_and_config_getter;
use crate::commands::run::CommandExitStatus;
use crate::config::config::ConfigFile;
use crate::error::summarise;

const MAX_ERRORS_TO_PROMPT_SUPPRESSION: usize = 100;

// This should likely be moved into config.rs
/// Types of configuration files that can be detected or created.
#[derive(Clone, Debug, Parser, Copy, Display)]
pub enum ConfigFileKind {
    MyPy,
    Pyright,
    Pyrefly,
    Pyproject,
}

impl ConfigFileKind {
    fn file_name(&self) -> &str {
        match self {
            Self::MyPy => "mypy.ini",
            Self::Pyright => "pyrightconfig.json",
            Self::Pyrefly => "pyrefly.toml",
            Self::Pyproject => "pyproject.toml",
        }
    }

    fn toml_identifier(self) -> String {
        match self {
            // This makes me question if pyproject should be a part of the enum at all
            Self::Pyproject => "".to_owned(),
            _ => format!("[tool.{self}]").to_lowercase(),
        }
    }
}

/// Initialize a new pyrefly config in the given directory. Can also be used to run pyrefly config-migration on a given project.
#[deny(clippy::missing_docs_in_private_items)]
#[derive(Clone, Debug, Parser)]
#[command(after_help = "Examples:
   `pyrefly init`: Create a new pyrefly.toml config in the current directory
 ")]
pub struct Args {
    /// The path to the project to initialize. Optional. If not present, will create a new pyrefly.toml config in the current directory.
    /// If this is the path to a pyproject.toml, the config will be written as a `[tool.pyrefly]` entry in that file.
    #[arg(default_value_os_t = PathBuf::from("."))]
    path: PathBuf,
}

impl Args {
    pub fn new(path: PathBuf) -> Self {
        Self { path }
    }

    pub fn new_migration(path: PathBuf) -> Self {
        Self { path }
    }

    fn check_for_pyproject_file(path: &Path) -> bool {
        if path.ends_with(ConfigFile::PYPROJECT_FILE_NAME) {
            return true;
        }
        let pyproject_path = &path.join(ConfigFile::PYPROJECT_FILE_NAME);
        pyproject_path.exists()
    }

    fn check_for_existing_config(path: &Path, kind: ConfigFileKind) -> anyhow::Result<bool> {
        let file_name = kind.file_name();
        if path.ends_with(file_name) && path.exists() {
            return Ok(true);
        }
        if path.ends_with(ConfigFile::PYPROJECT_FILE_NAME) && path.exists() {
            let raw_pyproject = fs_anyhow::read_to_string(path).with_context(|| {
                format!(
                    "While trying to check for an existing {} config in `{}`",
                    kind,
                    path.display()
                )
            })?;
            return Ok(raw_pyproject.contains(&kind.toml_identifier()));
        }
        if path.is_dir() {
            let custom_file = Args::check_for_existing_config(&path.join(file_name), kind);

            let pyproject =
                Args::check_for_existing_config(&path.join(ConfigFile::PYPROJECT_FILE_NAME), kind);
            return Ok(custom_file? || pyproject?);
        }
        Ok(false)
    }

    fn prompt_user_confirmation(prompt: &str) -> bool {
        if cfg!(test) {
            // decline confirmation, mocking user input
            return false;
        }
        let input = Self::read_from_stdin(prompt);
        let input = input.trim();
        input == "y" || input == "Y"
    }

    pub fn run(&self) -> anyhow::Result<CommandExitStatus> {
        // 1. Create Pyrefly Config
        let create_config_result = self.create_config();

        match create_config_result {
            Err(e) => Err(e),
            Ok((status, _)) if status != CommandExitStatus::Success => Ok(status),
            Ok((_, config_path)) => {
                // 2. Run pyrefly check
                let check_result = self.run_check(config_path.clone());

                // Check if there are errors and if there are fewer than 100
                if let Ok((_, errors)) = check_result {
                    let error_count = errors.len();
                    if error_count == 0 {
                        return Ok(CommandExitStatus::Success);
                    }
                    // 3a. Prompt error suppression if there are less than the maximum number of errors
                    else if error_count <= MAX_ERRORS_TO_PROMPT_SUPPRESSION {
                        return self.prompt_error_suppression(config_path, error_count);
                    }
                    // 3b. Prompt error suppression in specific subdirectories if there are more than the maximum number of errors
                    else {
                        return self.prompt_init_on_subdirectory(config_path, errors);
                    }
                }
                Ok(CommandExitStatus::Success)
            }
        }
    }

    fn run_check(
        &self,
        config_path: Option<PathBuf>,
    ) -> anyhow::Result<(CommandExitStatus, Vec<crate::error::error::Error>)> {
        info!("Running pyrefly check...");

        // Create check args by parsing arguments with output-format set to omit-errors
        let mut check_args = check::Args::parse_from(["check", "--output-format", "omit-errors"]);

        // Use get to get the filtered globs and config finder
        let (filtered_globs, config_finder) =
            globs_and_config_getter::get(Vec::new(), None, config_path, &mut check_args)?;

        // Run the check directly
        match check_args.run_once(filtered_globs, config_finder, true) {
            Ok((status, errors)) => Ok((status, errors)),
            Err(e) => {
                error!("Failed to run pyrefly check: {}", e);
                Ok((CommandExitStatus::Success, Vec::new())) // Still return success to match original behavior
            }
        }
    }

    fn prompt_error_suppression(
        &self,
        config_path: Option<PathBuf>,
        error_count: usize,
    ) -> anyhow::Result<CommandExitStatus> {
        let prompt =
            format!("Found {error_count} errors. Would you like to suppress them? (y/N): ");

        if Self::prompt_user_confirmation(&prompt) {
            info!("Running pyrefly check with suppress-errors flag...");

            // Create check args with suppress-errors flag
            let mut suppress_args = check::Args::parse_from([
                "check",
                "--suppress-errors",
                "--output-format",
                "omit-errors",
                "--no-summary",
            ]);

            // Use get to get the filtered globs and config finder
            let (suppress_globs, suppress_config_finder) =
                globs_and_config_getter::get(Vec::new(), None, config_path, &mut suppress_args)?;

            // Run the check with suppress-errors flag
            match suppress_args.run_once(suppress_globs, suppress_config_finder, true) {
                Ok(_) => return Ok(CommandExitStatus::Success),
                Err(e) => {
                    error!("Failed to run pyrefly check with suppress-errors: {}", e);
                    return Ok(CommandExitStatus::Success); // Still return success to match original behavior
                }
            }
        }

        Ok(CommandExitStatus::Success)
    }

    fn prompt_init_on_subdirectory(
        &self,
        config_path: Option<PathBuf>,
        errors: Vec<crate::error::error::Error>,
    ) -> anyhow::Result<CommandExitStatus> {
        // Get the top directories by error count
        let (best_path_index, dirs_to_show) =
            summarise::get_top_error_dirs_for_init(&errors, config_path.as_ref());

        // Print the top directories
        info!("Top 10 Directories by Error Count:");
        if !dirs_to_show.is_empty() {
            info!("  (Using path_index = {} for grouping)", best_path_index);

            // Take the top 10 directories with <= 100 errors
            for (i, (dir, error_count)) in dirs_to_show.iter().enumerate() {
                info!(
                    "  {}) {}: {}",
                    i + 1,
                    dir.display(),
                    display::count(*error_count, "error")
                );
            }
        } else {
            error!("  No directories found with <= 100 errors.");
            return Ok(CommandExitStatus::Success);
        }

        // Prompt user to select directories to suppress errors in
        let prompt = "Enter directory numbers to suppress errors (comma-separated, e.g. 1,3,5), or press Enter to skip: ";
        let selected_indices = Self::read_input_comma_separated_values(prompt, 1, 10);

        // If no valid directories were selected, return success
        if selected_indices.is_empty() {
            error!("No valid directory numbers provided. Skipping error suppression.");
            return Ok(CommandExitStatus::Success);
        }

        // Get the selected directories
        let selected_dirs: Vec<PathBuf> = selected_indices
            .iter()
            .filter_map(|&idx| {
                if idx < dirs_to_show.len() {
                    Some(dirs_to_show[idx - 1].0.clone())
                } else {
                    None
                }
            })
            .collect();

        // Print selected directories
        let dirs_str = if selected_dirs.len() == 1 {
            format!("directory {}", selected_dirs[0].display())
        } else {
            format!(
                "directories {}",
                selected_dirs
                    .iter()
                    .map(|d| d.display().to_string())
                    .collect::<Vec<_>>()
                    .join(", ")
            )
        };

        // Run check with suppress-errors for the selected directories
        info!(
            "Running pyrefly check with suppress-errors flag for selected directories: {}",
            dirs_str
        );

        // Create check args with suppress-errors flag
        let mut suppress_args = check::Args::parse_from([
            "check",
            "--suppress-errors",
            "--output-format",
            "omit-errors",
            "--no-summary",
        ]);

        // Collect file paths from errors in selected directories
        let mut files_to_check: Vec<String> = Vec::new();
        for error in &errors {
            let error_path = PathBuf::from(error.path().to_string());
            if selected_dirs.iter().any(|dir| error_path.starts_with(dir)) {
                // Convert PathBuf to String
                files_to_check.push(error_path.to_string_lossy().into_owned());
            }
        }

        // If there are no files to check in the selected directories, return success
        if files_to_check.is_empty() {
            error!("No errors found in the selected directories.");
            return Ok(CommandExitStatus::Success);
        }

        // Use get to get the filtered globs and config finder, passing the files to check
        let (suppress_globs, suppress_config_finder) =
            globs_and_config_getter::get(files_to_check, None, config_path, &mut suppress_args)?;

        // Run the check with suppress-errors flag
        match suppress_args.run_once(suppress_globs, suppress_config_finder, true) {
            Ok(_) => Ok(CommandExitStatus::Success),
            Err(e) => {
                error!("Failed to suppress errors: {}", e);
                Ok(CommandExitStatus::Success) // Still return success to match original behavior
            }
        }
    }

    fn create_config(&self) -> anyhow::Result<(CommandExitStatus, Option<PathBuf>)> {
        let path = self.path.absolutize()?.to_path_buf();

        let dir: Option<&Path> = if path.is_dir() {
            Some(&path)
        } else {
            path.parent()
        };
        if let Some(dir) = dir
            && Args::check_for_existing_config(dir, ConfigFileKind::Pyrefly)?
        {
            let prompt = format!(
                "The project at `{}` has already been initialized for pyrefly. Run `pyrefly check` to see type errors. Re-initialize and write a new section? (y/N): ",
                dir.display()
            );
            if !Self::prompt_user_confirmation(&prompt) {
                return Ok((CommandExitStatus::UserError, None));
            }
        }

        // 1. Check for mypy or pyright configuration
        let found_mypy = Args::check_for_existing_config(&path, ConfigFileKind::MyPy)?;
        let found_pyright = Args::check_for_existing_config(&path, ConfigFileKind::Pyright)?;

        // 2. Migrate existing configuration to Pyrefly configuration
        if found_mypy || found_pyright {
            println!("Found an existing type checking configuration - setting up pyrefly ...");
            let args = config_migration::Args {
                original_config_path: Some(path.clone()),
            };
            match args.run() {
                Ok((status, Some(config_path))) => return Ok((status, Some(config_path))),
                Ok((status, None)) => return Ok((status, None)),
                Err(e) => return Err(e),
            }
        }

        // Generate a basic config with a couple sensible defaults.
        // This prevents us from simply outputting an empty file, and gives the user somewhere to start if they want to customize.
        let cfg = ConfigFile {
            project_includes: ConfigFile::default_project_includes(),
            project_excludes: ConfigFile::default_project_excludes(),
            ..Default::default()
        };

        // 3. Initialize pyproject.toml configuration in the case that there are no existing Mypy or Pyright configurations but user specified a pyproject.toml
        if Args::check_for_pyproject_file(&path) {
            let config_path = if path.ends_with(ConfigFile::PYPROJECT_FILE_NAME) {
                path
            } else {
                path.join(ConfigFile::PYPROJECT_FILE_NAME)
            };
            write_pyproject(&config_path, cfg)?;
            info!("Config written to `{}`", config_path.display());
            return Ok((CommandExitStatus::Success, Some(config_path)));
        }

        // 4. Initialize pyrefly.toml configuration in the case that there are no existing Mypy or Pyright configurations and user didn't specify a pyproject.toml
        let config_path = if path.is_dir() {
            path.join(ConfigFile::PYREFLY_FILE_NAME)
        } else if path.ends_with(ConfigFile::PYREFLY_FILE_NAME) {
            path
        } else if !path.exists() {
            error!("Path `{}` does not exist", path.display());
            return Ok((CommandExitStatus::UserError, None));
        } else {
            error!(
                "Pyrefly configs must reside in `pyrefly.toml` or `pyproject.toml`, not `{}`",
                path.display()
            );
            return Ok((CommandExitStatus::UserError, None));
        };
        let serialized = toml::to_string_pretty(&cfg)?;
        fs_anyhow::write(&config_path, serialized.as_bytes())?;
        info!("New config written to `{}`", config_path.display());
        Ok((CommandExitStatus::Success, Some(config_path)))
    }

    fn read_from_stdin(prompt: &str) -> String {
        print!("{prompt}");
        std::io::stdout().flush().ok();

        // Read user input
        let mut input = String::new();
        std::io::stdin().read_line(&mut input).ok();
        input
    }

    fn read_input_comma_separated_values(prompt: &str, min: usize, max: usize) -> Vec<usize> {
        let input = Self::read_from_stdin(prompt);
        Self::parse_comma_separated_values(&input, min, max)
    }

    /// Parses comma-separated values from a string and returns a vector of parsed values
    /// within the specified range.
    ///
    /// # Arguments
    /// * `input` - The input string containing comma-separated values
    /// * `min` - The minimum valid value (inclusive)
    /// * `max` - The maximum valid value (inclusive)
    ///
    /// # Returns
    /// A vector of parsed values within the specified range
    fn parse_comma_separated_values(input: &str, min: usize, max: usize) -> Vec<usize> {
        let input = input.trim();

        // If input is empty, return empty vector
        if input.is_empty() {
            return Vec::new();
        }

        // Parse comma-separated values
        let selected_indices: Vec<usize> = input
            .split(',')
            .filter_map(|s| {
                let trimmed = s.trim();
                match trimmed.parse::<usize>() {
                    Ok(num) if (min..=max).contains(&num) => Some(num),
                    _ => {
                        warn!(
                            "'{}' is not a valid number ({}-{}), skipping.",
                            trimmed, min, max
                        );
                        None
                    }
                }
            })
            .collect();

        selected_indices
    }
}

#[cfg(test)]
mod test {
    use tempfile;
    use tempfile::TempDir;

    use super::*;

    // helper function for ConfigFile::from_file
    fn from_file(path: &Path) -> anyhow::Result<()> {
        let (_, errs) = ConfigFile::from_file(path);
        if errs.is_empty() {
            Ok(())
        } else {
            for e in errs {
                e.print();
            }
            Err(anyhow::anyhow!(format!(
                "ConfigFile::from_file({}) failed",
                path.display(),
            )))
        }
    }

    fn run_init_on_dir(dir: &TempDir) -> anyhow::Result<CommandExitStatus> {
        let args = Args::new(dir.path().to_path_buf());
        args.run()
    }

    fn run_init_on_file(dir: &TempDir, file: &str) -> anyhow::Result<CommandExitStatus> {
        let args = Args::new(dir.path().join(file));
        args.run()
    }

    fn assert_success(status: CommandExitStatus) {
        assert!(matches!(status, CommandExitStatus::Success), "{status:#?}");
    }

    fn assert_user_error(status: CommandExitStatus) {
        assert!(
            matches!(status, CommandExitStatus::UserError),
            "{status:#?}"
        );
    }

    fn create_file_in(dir: &Path, filename: &str, contents: Option<&[u8]>) -> anyhow::Result<()> {
        let pyrefly_toml = dir.join(filename);
        let contents = contents.unwrap_or(b"");
        fs_anyhow::write(&pyrefly_toml, contents)
    }

    fn check_file_in(dir: &Path, filename: &str, contents: &[&str]) -> anyhow::Result<()> {
        let fi = dir.join(filename);
        let raw_cfg = fs_anyhow::read_to_string(&fi)?;
        for snippet in contents {
            assert!(raw_cfg.contains(snippet), "{snippet}");
        }
        from_file(&fi)
    }

    #[test]
    fn test_empty_dir() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        let status = run_init_on_dir(&tmp)?;
        assert_success(status);
        check_file_in(tmp.path(), "pyrefly.toml", &["project-includes"])
    }

    #[test]
    fn test_path_to_new_pyrefly_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        let status = run_init_on_file(&tmp, "pyrefly.toml")?;
        assert_success(status);
        check_file_in(tmp.path(), "pyrefly.toml", &["project-includes"])
    }

    #[test]
    fn test_dir_with_existing_pyrefly_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(tmp.path(), "pyrefly.toml", None)?;
        let status = run_init_on_dir(&tmp)?;
        assert_user_error(status);
        Ok(())
    }

    #[test]
    fn test_path_to_existing_pyrefly_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(tmp.path(), "pyrefly.toml", None)?;
        let status = run_init_on_file(&tmp, "pyrefly.toml")?;
        assert_user_error(status);
        Ok(())
    }

    #[test]
    fn test_dir_with_mypy_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(tmp.path(), "mypy.ini", Some(b"[mypy]\nfiles = abc"))?;
        let status = run_init_on_dir(&tmp)?;
        assert_success(status);
        check_file_in(
            tmp.path(),
            "pyrefly.toml",
            &["project-includes = [\"abc\"]"],
        )
    }

    #[test]
    fn test_path_to_mypy_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(tmp.path(), "mypy.ini", Some(b"[mypy]\nfiles = abc"))?;
        let status = run_init_on_file(&tmp, "mypy.ini")?;
        assert_success(status);
        check_file_in(
            tmp.path(),
            "pyrefly.toml",
            &["project-includes = [\"abc\"]"],
        )
    }

    #[test]
    fn test_path_to_nonexistent_mypy_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        let status = run_init_on_file(&tmp, "mypy.ini")?;
        assert_user_error(status);
        Ok(())
    }

    #[test]
    fn test_dir_with_pyright_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(
            tmp.path(),
            "pyrightconfig.json",
            Some(
                b"\
{
    \"include\": [\"abc\"]
}",
            ),
        )?;
        let status = run_init_on_dir(&tmp)?;
        assert_success(status);
        check_file_in(
            tmp.path(),
            "pyrefly.toml",
            &["project-includes = [\"abc\"]"],
        )
    }

    #[test]
    fn test_path_to_pyright_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(
            tmp.path(),
            "pyrightconfig.json",
            Some(
                b"\
{
    \"include\": [\"abc\"]
}",
            ),
        )?;
        let status = run_init_on_file(&tmp, "pyrightconfig.json")?;
        assert_success(status);
        check_file_in(
            tmp.path(),
            "pyrefly.toml",
            &["project-includes = [\"abc\"]"],
        )
    }

    #[test]
    fn test_path_to_nonexistent_pyright_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        let status = run_init_on_file(&tmp, "pyrightconfig.json")?;
        assert_user_error(status);
        Ok(())
    }

    #[test]
    fn test_dir_with_pyproject_toml_no_typechecking_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(
            tmp.path(),
            "pyproject.toml",
            Some(
                b"\
[tool.random_project]
k = \"v\"
",
            ),
        )?;
        let status = run_init_on_dir(&tmp)?;
        assert_success(status);
        check_file_in(
            tmp.path(),
            "pyproject.toml",
            &["tool.random_project", "tool.pyrefly"],
        )
    }

    #[test]
    fn test_dir_with_pyproject_toml_mypy_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(
            tmp.path(),
            "pyproject.toml",
            Some(
                b"\
[tool.mypy]
files = \"abc\"
",
            ),
        )?;
        let status = run_init_on_dir(&tmp)?;
        assert_success(status);
        check_file_in(
            tmp.path(),
            "pyproject.toml",
            &["tool.mypy", "tool.pyrefly", "project-includes = [\"abc\"]"],
        )
    }

    #[test]
    fn test_dir_with_pyproject_toml_pyright_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(
            tmp.path(),
            "pyproject.toml",
            Some(
                b"\
[tool.pyright]
include = [\"abc\"]
",
            ),
        )?;
        let status = run_init_on_dir(&tmp)?;
        assert_success(status);
        check_file_in(
            tmp.path(),
            "pyproject.toml",
            &[
                "tool.pyright",
                "tool.pyrefly",
                "project-includes = [\"abc\"]",
            ],
        )
    }

    #[test]
    fn test_path_to_pyproject_toml_pyright_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(
            tmp.path(),
            "pyproject.toml",
            Some(
                b"\
[tool.pyright]
include = [\"abc\"]
",
            ),
        )?;
        let status = run_init_on_file(&tmp, "pyproject.toml")?;
        assert_success(status);
        check_file_in(
            tmp.path(),
            "pyproject.toml",
            &[
                "tool.pyright",
                "tool.pyrefly",
                "project-includes = [\"abc\"]",
            ],
        )
    }

    #[test]
    fn test_path_to_pyproject_toml_no_typechecking_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(
            tmp.path(),
            "pyproject.toml",
            Some(
                b"\
[tool.random_project]
k = [\"v\"]
",
            ),
        )?;
        let status = run_init_on_file(&tmp, "pyproject.toml")?;
        assert_success(status);
        check_file_in(
            tmp.path(),
            "pyproject.toml",
            &["tool.random_project", "tool.pyrefly"],
        )
    }

    #[test]
    fn test_path_to_nonexistent_pyproject_toml() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        let status = run_init_on_file(&tmp, "pyproject.toml")?;
        assert_success(status);
        check_file_in(tmp.path(), "pyproject.toml", &["tool.pyrefly"])
    }

    #[test]
    fn test_dir_with_pyproject_toml_existing_pyrefly_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(tmp.path(), "pyproject.toml", Some(b"[tool.pyrefly]"))?;
        let status = run_init_on_dir(&tmp)?;
        assert_user_error(status);
        Ok(())
    }

    #[test]
    fn test_path_to_pyproject_toml_existing_pyrefly_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(tmp.path(), "pyproject.toml", Some(b"[tool.pyrefly]"))?;
        let status = run_init_on_file(&tmp, "pyproject.toml")?;
        assert_user_error(status);
        Ok(())
    }

    #[test]
    fn test_config_file_kinds() -> anyhow::Result<()> {
        let kind = ConfigFileKind::MyPy;
        assert_eq!(kind.toml_identifier(), "[tool.mypy]".to_owned());
        Ok(())
    }

    #[test]
    fn test_bad_path() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        let status = run_init_on_file(&tmp, "personal_configs.json")?;
        assert_user_error(status);
        Ok(())
    }

    #[test]
    fn test_mypy_config_twice() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(tmp.path(), "mypy.ini", None)?;
        let status1 = run_init_on_file(&tmp, "mypy.ini")?;
        assert_success(status1);
        let status2 = run_init_on_file(&tmp, "mypy.ini")?;
        assert_user_error(status2);
        Ok(())
    }

    #[test]
    fn test_pyproject_toml_with_existing_pyrefly_config() -> anyhow::Result<()> {
        let tmp = tempfile::tempdir()?;
        create_file_in(tmp.path(), "pyrefly.toml", None)?;
        let status = run_init_on_file(&tmp, "pyproject.toml")?;
        assert_user_error(status);
        Ok(())
    }

    // Test for parse_comma_separated_values with multiple test cases
    #[test]
    fn test_parse_comma_separated_values() {
        // Define test cases as (input, min, max, expected_result)
        let test_cases = [
            // Empty input
            ("", 1, 10, vec![]),
            // Single valid number
            ("5", 1, 10, vec![5]),
            // Multiple valid numbers
            ("1,3,5,10", 1, 10, vec![1, 3, 5, 10]),
            // Input with spaces
            (" 1, 3 , 5,  10 ", 1, 10, vec![1, 3, 5, 10]),
            // Out of range values
            ("0,11,15", 1, 10, vec![]),
            // Mixed valid and invalid values
            ("0,3,11,5", 1, 10, vec![3, 5]),
            // Non-numeric values
            ("a,b,c", 1, 10, vec![]),
            // Mixed numeric and non-numeric values
            ("1,a,3,b,5", 1, 10, vec![1, 3, 5]),
            // Custom range
            ("4,5,10,15,16", 5, 15, vec![5, 10, 15]),
        ];

        // Run each test case
        for (i, (input, min, max, expected)) in test_cases.iter().enumerate() {
            let result = Args::parse_comma_separated_values(input, *min, *max);
            assert_eq!(
                result, *expected,
                "Test case {i} failed: input='{input}', min={min}, max={max}",
            );
        }
    }
}
