# SPDX-PackageName: gel-python
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright Gel Data Inc. and the contributors.


STATE = """
SELECT
    {
        server_version := (
            WITH v := sys::get_version()
            SELECT (major := v.major, minor := v.minor)
        ),
        top_migration := assert_single((
            WITH MODULE schema
            SELECT Migration FILTER NOT EXISTS .<parents[IS Migration]
        ).name)
    }
"""


MODULES = """
WITH
    MODULE schema,
    m := (SELECT `Module` FILTER .builtin = <bool>$builtin)
SELECT
    _ := m.name
ORDER BY
    _;
"""


GLOBALS = """
WITH
    MODULE schema,
SELECT schema::Global {
    id,
    name,
    description := assert_single((
        WITH
            tid := .id,
        SELECT DETACHED Operator {
            description := (SELECT .annotations {
                value := materialized(@value)
            } FILTER .name = "std::description"),
        } FILTER .id = tid
    ).description.value),
    type := (
        IF .target.from_alias AND .target IS InheritingObject
        THEN assert_single(.target[IS InheritingObject].bases)
        ELSE .target
    ),
    required,
    cardinality,
}
FILTER
    .builtin = <bool>$builtin
ORDER BY
    .name
"""


CASTS = """
WITH
    MODULE schema
SELECT Cast {
    id,
    from_type,
    to_type,
    allow_assignment,
    allow_implicit,
}
FILTER
    .from_type IS ScalarType
    AND .to_type IS ScalarType
    AND .builtin = <bool>$builtin
"""


OPERATORS = """
WITH
    MODULE schema,
SELECT Operator {
    id,
    name,
    description := assert_single((
        WITH
            tid := .id,
        SELECT DETACHED Operator {
            description := (SELECT .annotations {
                value := materialized(@value)
            } FILTER .name = "std::description"),
        } FILTER .id = tid
    ).description.value),
    suggested_ident := assert_single((
        WITH
            tid := .id,
        SELECT DETACHED Operator {
            identifier := (SELECT .annotations {
                value := materialized(@value)
            } FILTER .name = "std::identifier"),
        } FILTER .id = tid
    ).identifier.value),
    operator_kind,
    return_type,
    return_typemod,
    params: {
        name,
        type,
        kind,
        typemod,
        default,
        index := @index,
    } ORDER BY @index,
}
FILTER
    .builtin = <bool>$builtin
    AND NOT .internal
"""


FUNCTIONS = """
WITH
    MODULE schema,
SELECT Function {
    id,
    name,
    description := assert_single((
        WITH
            tid := .id,
        SELECT DETACHED Operator {
            description := (SELECT .annotations {
                value := materialized(@value)
            } FILTER .name = "std::description"),
        } FILTER .id = tid
    ).description.value),
    return_type,
    return_typemod,
    params: {
        name,
        type,
        kind,
        typemod,
        default,
        index := @index,
    } ORDER BY @index,
    preserves_optionality,
}
FILTER
    .builtin = <bool>$builtin
    AND NOT .internal
"""


TYPES = """
WITH
    MODULE schema,

    material_scalars := (
        SELECT ScalarType
        FILTER
            NOT .abstract
            AND NOT EXISTS .enum_values
            AND NOT EXISTS (SELECT .ancestors FILTER NOT .abstract)
    )

SELECT Type {
    kind := assert_exists(
        'Object' IF Type IS ObjectType ELSE
        'Scalar' IF Type IS ScalarType ELSE
        'Array' IF Type IS Array ELSE
        'NamedTuple' IF Type[IS Tuple].named ?? false ELSE
        'Tuple' IF Type IS Tuple ELSE
        'Range' IF Type IS Range ELSE
        'MultiRange' IF Type IS MultiRange ELSE
        'Pseudo' IF Type IS PseudoType ELSE
        <str>{},
        message := "unexpected type",
    ),

    id,
    builtin,
    internal,

    name := (
        array_join(array_agg([IS ObjectType].union_of.name), ' | ')
        IF EXISTS [IS ObjectType].union_of
        ELSE .name
    ),

    description := assert_single((
        WITH
            tid := .id,
        SELECT (ScalarType UNION ObjectType) {
            description := (SELECT .annotations {
                value := materialized(@value)
            } FILTER .name = "std::description"),
        } FILTER .id = tid
    ).description.value),

    [IS SubclassableObject].abstract,
    [IS SubclassableObject].final,

    expr,
    from_alias,

    [IS ScalarType].enum_values,
    is_seq := 'std::sequence' in [IS ScalarType].ancestors.name,

    # for sequence (abstract type that has non-abstract ancestor)
    single material_id := (
        SELECT Type[IS ScalarType].ancestors
        FILTER NOT .abstract
        ORDER BY @index ASC
        LIMIT 1
    ).id,

    [IS InheritingObject].bases: {
        id
    } ORDER BY @index ASC,

    [IS InheritingObject].ancestors: {
        id
    } ORDER BY @index ASC,

    [IS ObjectType].compound_type,
    [IS ObjectType].union_of,
    [IS ObjectType].intersection_of,
    [IS ObjectType].pointers: {
        id,
        card := ("One" IF .required ELSE "AtMostOne")
                IF <str>.cardinality = "One"
                ELSE ("AtLeastOne" IF .required ELSE "Many"),
        name,
        target_id := .target.id,
        kind := 'Link' IF .__type__.name = 'schema::Link' ELSE 'Property',
        is_exclusive := EXISTS (SELECT .constraints
                                FILTER .name = 'std::exclusive'),
        is_computed := len(.computed_fields) != 0,
        is_readonly := .readonly,
        has_default := (
            EXISTS .default
            OR ("std::sequence" IN .target[IS ScalarType].ancestors.name)
        ),
        [IS Link].pointers: {
            id,
            card := ("One" IF .required ELSE "AtMostOne")
                    IF <str>.cardinality = "One"
                    ELSE ("AtLeastOne" IF .required ELSE "Many"),
            name,
            target_id := .target.id,
            kind := 'Property',
            is_exclusive := EXISTS (SELECT .constraints
                                    FILTER .name = 'std::exclusive'),
            is_computed := len(.computed_fields) != 0,
            is_readonly := .readonly,
            has_default := (
                EXISTS .default
                OR ("std::sequence" IN .target[IS ScalarType].ancestors.name)
            ),
        } FILTER .name != 'source' AND .name != 'target'
    } FILTER any(@is_owned),
    exclusives := assert_distinct((
        [IS schema::ObjectType].constraints
        UNION
        [IS schema::ObjectType].pointers.constraints
    ) {
        target := (.subject[is schema::Property].name
                   ?? .subject[is schema::Link].name
                   ?? .subjectexpr)
    } FILTER .name = 'std::exclusive'),
    array_element_id := [IS Array].element_type.id,

    tuple_elements := (SELECT [IS Tuple].element_types {
        type_id := .type.id,
        name
    } ORDER BY @index ASC),
    range_element_id := [IS Range].element_type.id,
    multirange_element_id := [IS MultiRange].element_type.id,
}
FILTER
    .builtin = <bool>$builtin
    AND NOT .from_alias
ORDER BY
    .name;
"""
