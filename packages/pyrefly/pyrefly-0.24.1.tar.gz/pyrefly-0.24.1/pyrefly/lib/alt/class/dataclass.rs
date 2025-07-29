/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use std::sync::Arc;

use pyrefly_python::dunder;
use ruff_python_ast::name::Name;
use ruff_text_size::TextRange;
use starlark_map::small_map::SmallMap;
use starlark_map::small_set::SmallSet;

use crate::alt::answers::LookupAnswer;
use crate::alt::answers_solver::AnswersSolver;
use crate::alt::class::class_field::ClassField;
use crate::alt::class::class_field::DataclassMember;
use crate::alt::types::class_metadata::ClassMetadata;
use crate::alt::types::class_metadata::ClassSynthesizedField;
use crate::alt::types::class_metadata::ClassSynthesizedFields;
use crate::alt::types::class_metadata::DataclassMetadata;
use crate::error;
use crate::error::collector::ErrorCollector;
use crate::error::context::TypeCheckContext;
use crate::error::context::TypeCheckKind;
use crate::error::kind::ErrorKind;
use crate::types::callable::Callable;
use crate::types::callable::FuncMetadata;
use crate::types::callable::Function;
use crate::types::callable::Param;
use crate::types::callable::ParamList;
use crate::types::callable::Required;
use crate::types::class::Class;
use crate::types::class::ClassType;
use crate::types::display::ClassDisplayContext;
use crate::types::keywords::DataclassFieldKeywords;
use crate::types::keywords::TypeMap;
use crate::types::literal::Lit;
use crate::types::tuple::Tuple;
use crate::types::types::AnyStyle;
use crate::types::types::Type;

impl<'a, Ans: LookupAnswer> AnswersSolver<'a, Ans> {
    /// Gets dataclass fields for an `@dataclass`-decorated class.
    pub fn get_dataclass_fields(
        &self,
        cls: &Class,
        bases_with_metadata: &[(ClassType, Arc<ClassMetadata>)],
    ) -> SmallSet<Name> {
        let mut all_fields = SmallSet::new();
        for (_, metadata) in bases_with_metadata.iter().rev() {
            if let Some(dataclass) = metadata.dataclass_metadata() {
                all_fields.extend(dataclass.fields.clone());
            }
        }
        for name in cls.fields() {
            if cls.is_field_annotated(name) {
                all_fields.insert(name.clone());
            }
        }
        all_fields
    }

    pub fn get_dataclass_synthesized_fields(
        &self,
        cls: &Class,
        errors: &ErrorCollector,
    ) -> Option<ClassSynthesizedFields> {
        let metadata = self.get_metadata_for_class(cls);
        let dataclass = metadata.dataclass_metadata()?;
        let mut fields = SmallMap::new();
        if dataclass.kws.init {
            fields.insert(
                dunder::INIT,
                self.get_dataclass_init(cls, dataclass, errors),
            );
        }
        let dataclass_fields_type = self.stdlib.dict(
            self.stdlib.str().clone().to_type(),
            Type::Any(AnyStyle::Implicit),
        );
        fields.insert(
            dunder::DATACLASS_FIELDS,
            ClassSynthesizedField::new(dataclass_fields_type.to_type()),
        );

        if dataclass.kws.order {
            fields.extend(self.get_dataclass_rich_comparison_methods(cls));
        }
        if dataclass.kws.match_args {
            fields.insert(
                dunder::MATCH_ARGS,
                self.get_dataclass_match_args(cls, dataclass),
            );
        }
        if dataclass.kws.slots {
            // It's a runtime error to set slots=True on a class that already defines __slots__.
            // Note that inheriting __slots__ from a base class is fine.
            if cls.contains(&dunder::SLOTS) {
                self.error(
                    errors,
                    cls.range(),
                    ErrorKind::BadClassDefinition,
                    None,
                    "Cannot specify both `slots=True` and `__slots__`".to_owned(),
                );
            } else {
                fields.insert(dunder::SLOTS, self.get_dataclass_slots(cls, dataclass));
            }
        }
        // See rules for `__hash__` creation under "unsafe_hash":
        // https://docs.python.org/3/library/dataclasses.html#module-contents
        if dataclass.kws.unsafe_hash || (dataclass.kws.eq && dataclass.kws.frozen) {
            fields.insert(dunder::HASH, self.get_dataclass_hash(cls));
        } else if dataclass.kws.eq {
            fields.insert(dunder::HASH, ClassSynthesizedField::new(Type::None));
        }
        Some(ClassSynthesizedFields::new(fields))
    }

    pub fn validate_frozen_dataclass_inheritance(
        &self,
        cls: &Class,
        dataclass_metadata: &DataclassMetadata,
        bases_with_metadata: &[(ClassType, Arc<ClassMetadata>)],
        errors: &ErrorCollector,
    ) {
        for (base_type, base_metadata) in bases_with_metadata {
            if let Some(base_dataclass_metadata) = base_metadata.dataclass_metadata() {
                let is_base_frozen = base_dataclass_metadata.kws.frozen;
                let is_current_frozen = dataclass_metadata.kws.frozen;

                if is_current_frozen != is_base_frozen {
                    let current_status = if is_current_frozen {
                        "frozen"
                    } else {
                        "non-frozen"
                    };
                    let base_status = if is_base_frozen {
                        "frozen"
                    } else {
                        "non-frozen"
                    };

                    let base = base_type.class_object();
                    let ctx = ClassDisplayContext::new(&[cls, base]);
                    self.error(
                        errors,
                        cls.range(),
                        ErrorKind::InvalidInheritance,
                        None,
                        format!(
                            "Cannot inherit {} dataclass `{}` from {} dataclass `{}`",
                            current_status,
                            ctx.display(cls),
                            base_status,
                            ctx.display(base),
                        ),
                    );
                }
            }
        }
    }

    pub fn validate_post_init(
        &self,
        cls: &Class,
        dataclass_metadata: &DataclassMetadata,
        post_init: Type,
        range: TextRange,
        errors: &ErrorCollector,
    ) {
        // `__post_init__` is called with a dataclass's `InitVar`s, so we use the `InitVar` types
        // to generate a callable signature to check `__post_init__` against.
        let mut params = Vec::new();
        for (name, field, _) in self.iter_fields(cls, dataclass_metadata, true) {
            if field.is_init_var() {
                params.push(field.as_param(&name, false, false, None));
            }
        }
        let want = Type::Callable(Box::new(Callable::list(
            ParamList::new(params),
            self.stdlib.object().clone().to_type(),
        )));
        self.check_type(&want, &post_init, range, errors, &|| {
            TypeCheckContext::of_kind(TypeCheckKind::PostInit)
        });
    }

    pub fn dataclass_field_keywords(&self, map: &TypeMap) -> DataclassFieldKeywords {
        let init = map.get_bool(&DataclassFieldKeywords::INIT, true);
        let default = [
            &DataclassFieldKeywords::DEFAULT,
            &DataclassFieldKeywords::DEFAULT_FACTORY,
            &DataclassFieldKeywords::FACTORY,
        ]
        .iter()
        .any(|k| map.0.contains_key(*k));
        let kw_only = map
            .0
            .get(&DataclassFieldKeywords::KW_ONLY)
            .and_then(|t| t.as_bool());
        let alias = map
            .get_string(&DataclassFieldKeywords::ALIAS)
            .map(Name::new);
        let converter_param = self.get_converter_param(map);
        DataclassFieldKeywords {
            init,
            default,
            kw_only,
            alias,
            converter_param,
        }
    }

    fn get_converter_param(&self, map: &TypeMap) -> Option<Type> {
        let converter = {
            let converter = map.0.get(&DataclassFieldKeywords::CONVERTER)?;
            if let Type::ClassDef(cls) = converter
                && let Type::ClassType(instance) = self.instantiate_fresh(cls)
            {
                let callable = self.constructor_to_callable(&instance);
                &self.distribute_over_union(&callable, |ty| {
                    if let Type::BoundMethod(m) = ty {
                        m.to_callable().unwrap_or_else(|| ty.clone())
                    } else {
                        ty.clone()
                    }
                })
            } else {
                converter
            }
        };
        Some(self.distribute_over_union(converter, |ty| {
            ty.callable_first_param().unwrap_or_else(Type::any_implicit)
        }))
    }

    fn iter_fields(
        &self,
        cls: &Class,
        dataclass: &DataclassMetadata,
        include_initvar: bool,
    ) -> Vec<(Name, ClassField, DataclassFieldKeywords)> {
        let mut seen_kw_only_marker = false;
        let mut positional_fields = Vec::new();
        let mut kwonly_fields = Vec::new();
        let cls_is_kw_only = dataclass.kws.kw_only;
        for name in dataclass.fields.iter() {
            match (self.get_dataclass_member(cls, name), include_initvar) {
                (DataclassMember::KwOnlyMarker, _) => {
                    seen_kw_only_marker = true;
                }
                (DataclassMember::NotAField, _) => {}
                (DataclassMember::Field(field, mut keywords), _)
                | (DataclassMember::InitVar(field, mut keywords), true) => {
                    if keywords.kw_only.is_none() {
                        // kw_only hasn't been explicitly set on the field
                        keywords.kw_only = Some(
                            seen_kw_only_marker || (cls_is_kw_only && field.defining_class == *cls),
                        );
                    };
                    if keywords.is_kw_only() {
                        kwonly_fields.push((name.clone(), (*field.value).clone(), keywords))
                    } else {
                        positional_fields.push((name.clone(), (*field.value).clone(), keywords))
                    }
                }
                (DataclassMember::InitVar(..), false) => {}
            }
        }
        positional_fields.extend(kwonly_fields);
        positional_fields
    }

    /// Gets __init__ method for an `@dataclass`-decorated class.
    fn get_dataclass_init(
        &self,
        cls: &Class,
        dataclass: &DataclassMetadata,
        errors: &ErrorCollector,
    ) -> ClassSynthesizedField {
        let mut params = vec![self.class_self_param(cls, false)];
        let mut has_seen_default = false;
        for (name, field, field_flags) in self.iter_fields(cls, dataclass, true) {
            if field_flags.init {
                let has_default = field_flags.default;
                let is_kw_only = field_flags.is_kw_only();
                if !is_kw_only {
                    if !has_default
                        && has_seen_default
                        && let Some(range) = cls.field_decl_range(&name)
                    {
                        self.error(
                                errors,
                                range,
                                error::kind::ErrorKind::BadClassDefinition,
                                None,
                                format!(
                                    "Dataclass field `{name}` without a default may not follow dataclass field with a default"
                                ),
                            );
                    }
                    if has_default {
                        has_seen_default = true;
                    }
                }
                params.push(field.as_param(
                    &field_flags.alias.unwrap_or(name),
                    has_default,
                    is_kw_only,
                    field_flags.converter_param,
                ));
            }
        }

        let ty = Type::Function(Box::new(Function {
            signature: Callable::list(ParamList::new(params), Type::None),
            metadata: FuncMetadata::def(
                self.module_info().name(),
                cls.name().clone(),
                dunder::INIT,
            ),
        }));
        ClassSynthesizedField::new(ty)
    }

    fn get_dataclass_match_args(
        &self,
        cls: &Class,
        dataclass: &DataclassMetadata,
    ) -> ClassSynthesizedField {
        // Keyword-only fields do not appear in __match_args__.
        let kw_only = dataclass.kws.kw_only;
        let ts = if kw_only {
            Vec::new()
        } else {
            let filtered_fields = self.iter_fields(cls, dataclass, true);
            filtered_fields
                .iter()
                .filter_map(|(name, _, field_flags)| {
                    if field_flags.is_kw_only() || !field_flags.init {
                        None
                    } else {
                        Some(Type::Literal(Lit::Str(name.as_str().into())))
                    }
                })
                .collect()
        };
        let ty = Type::Tuple(Tuple::Concrete(ts));
        ClassSynthesizedField::new(ty)
    }

    fn get_dataclass_slots(
        &self,
        cls: &Class,
        dataclass: &DataclassMetadata,
    ) -> ClassSynthesizedField {
        let filtered_fields = self.iter_fields(cls, dataclass, false);
        let ts = filtered_fields
            .iter()
            .map(|(name, _, _)| Type::Literal(Lit::Str(name.as_str().into())))
            .collect();
        let ty = Type::Tuple(Tuple::Concrete(ts));
        ClassSynthesizedField::new(ty)
    }

    fn get_dataclass_rich_comparison_methods(
        &self,
        cls: &Class,
    ) -> SmallMap<Name, ClassSynthesizedField> {
        let make_signature = |other_type| {
            let other = Param::Pos(Name::new_static("other"), other_type, Required::Required);
            Callable::list(
                ParamList::new(vec![self.class_self_param(cls, false), other]),
                self.stdlib.bool().clone().to_type(),
            )
        };
        let callable = make_signature(self.instantiate(cls));
        let callable_eq = make_signature(self.stdlib.object().clone().to_type());
        dunder::RICH_CMPS
            .iter()
            .map(|name| {
                (
                    name.clone(),
                    ClassSynthesizedField::new(Type::Function(Box::new(Function {
                        signature: if *name == dunder::EQ || *name == dunder::NE {
                            callable_eq.clone()
                        } else {
                            callable.clone()
                        },
                        metadata: FuncMetadata::def(
                            self.module_info().name(),
                            cls.name().clone(),
                            name.clone(),
                        ),
                    }))),
                )
            })
            .collect()
    }

    fn get_dataclass_hash(&self, cls: &Class) -> ClassSynthesizedField {
        let params = vec![self.class_self_param(cls, false)];
        let ret = self.stdlib.int().clone().to_type();
        ClassSynthesizedField::new(Type::Function(Box::new(Function {
            signature: Callable::list(ParamList::new(params), ret),
            metadata: FuncMetadata::def(
                self.module_info().name(),
                cls.name().clone(),
                dunder::HASH,
            ),
        })))
    }
}
