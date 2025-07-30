# SPDX-PackageName: gel-python
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright Gel Data Inc. and the contributors.

"""Typing generics for the EdgeQL query builder."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    TypedDict,
    get_args,
)


import dataclasses
import functools
import inspect
import types

from gel._internal import _edgeql
from gel._internal import _namespace
from gel._internal import _typing_inspect
from gel._internal import _utils

from ._abstract import AbstractDescriptor, AbstractFieldDescriptor
from ._expressions import (
    BinaryOp,
    Global,
    Path,
    Variable,
    get_object_type_splat,
    toplevel_edgeql,
)
from ._protocols import (
    TypeClassProto,
    assert_edgeql_qb_expr,
    edgeql_qb_expr,
    is_exprmethod,
)
from ._reflection import GelTypeMetadata

if TYPE_CHECKING:
    from collections.abc import Iterable

    from gel._internal._schemapath import SchemaPath
    from ._abstract import Expr


_OP_OVERLOADS = frozenset(
    {
        "__add__",
        "__and__",
        "__divmod__",
        "__eq__",
        "__floordiv__",
        "__ge__",
        "__getitem__",
        "__gt__",
        "__le__",
        "__lshift__",
        "__lt__",
        "__matmul__",
        "__mod__",
        "__mul__",
        "__ne__",
        "__or__",
        "__pow__",
        "__rshift__",
        "__sub__",
        "__truediv__",
        "__xor__",
    }
)
"""Operators that are overloaded on types"""

_SWAPPED_OP_OVERLOADS = frozenset(
    {
        "__radd__",
        "__rand__",
        "__rfloordiv__",
        "__rlshift__",
        "__rmatmul__",
        "__rmod__",
        "__rmul__",
        "__ror__",
        "__rpow__",
        "__rrshift__",
        "__rsub__",
        "__rtruediv__",
        "__rxor__",
    }
)
"""Operators that are overloaded on types (swapped versions)"""


class _BinaryOpKwargs(TypedDict, total=False):
    lexpr: Expr
    rexpr: Expr
    op: _edgeql.Token
    type_: SchemaPath


SPECIAL_EXPR_METHODS = frozenset(
    {
        "__gel_assert_single__",
    }
)


class BaseAliasMeta(type):
    def __new__(
        mcls,
        name: str,
        bases: tuple[type[Any], ...],
        namespace: dict[str, Any],
    ) -> BaseAliasMeta:
        for op in _OP_OVERLOADS:
            namespace.setdefault(
                op,
                lambda self, other, op=op: self.__infix_op__(op, other),
            )

        for op in _SWAPPED_OP_OVERLOADS:
            namespace.setdefault(
                op,
                lambda self, other, op=op: self.__infix_op__(
                    op, other, swapped=True
                ),
            )

        return super().__new__(mcls, name, bases, namespace)


class BaseAlias(metaclass=BaseAliasMeta):
    def __init__(self, origin: type[TypeClassProto], metadata: Expr) -> None:
        self.__gel_origin__ = origin
        self.__gel_metadata__ = metadata
        if _typing_inspect.is_generic_alias(origin):
            real_origin = get_args(origin)[0]
        else:
            real_origin = origin
        proxied_dunders: Iterable[str] = (
            getattr(real_origin, "__gel_proxied_dunders__", ()) or ()
        )
        self.__gel_proxied_dunders__ = frozenset(proxied_dunders)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.__gel_origin__(*args, **kwargs)

    def __mro_entries__(self, bases: tuple[type, ...]) -> tuple[type, ...]:
        return (self.__gel_origin__,)

    def __dir__(self) -> list[str]:
        return dir(self.__gel_origin__)

    def __instancecheck__(self, obj: object) -> bool:
        return isinstance(obj, self.__gel_origin__)

    def __subclasscheck__(self, cls: type) -> bool:
        return issubclass(cls, self.__gel_origin__)  # pyright: ignore [reportGeneralTypeIssues]

    def __repr__(self) -> str:
        origin = _utils.type_repr(self.__gel_origin__)
        metadata = repr(self.__gel_metadata__)
        return f"{_utils.type_repr(type(self))}[{origin}, {metadata}]"

    def __getattr__(self, attr: str) -> Any:
        if attr == "link":
            # `default.MyType.linkname.link()` is a very common operation:
            # it can be called millions of times when loading data and
            # the descriptor lookup with the subsequent `.get()` slow down
            # instance creation ~40%.
            #
            # Given that "link" is a reserved EdgeQL keyword, we can just
            # resolve it to `ProxyModel.link()` as fast as possible.
            try:
                method = type.__getattribute__(self.__gel_origin__, "link")
            except AttributeError:
                # Alright, let's try the descriptor lookup.
                pass
            else:
                if isinstance(method, types.MethodType):
                    # Got it -- cache it so it's even faster next time.
                    object.__setattr__(self, "link", method)
                    return method

        if (
            not _namespace.is_dunder(attr)
            or attr in self.__gel_proxied_dunders__
            or attr in SPECIAL_EXPR_METHODS
        ):
            origin = self.__gel_origin__
            descriptor = inspect.getattr_static(origin, attr, None)
            if isinstance(descriptor, AbstractFieldDescriptor):
                return descriptor.get(origin, self)
            else:
                attrval = getattr(origin, attr)
                if is_exprmethod(attrval):

                    @functools.wraps(attrval)
                    def wrapper(*args: Any, **kwargs: Any) -> Any:
                        return attrval(*args, __operand__=self, **kwargs)

                    return wrapper
                else:
                    return attrval
        else:
            raise AttributeError(attr)

    def __edgeql_qb_expr__(self) -> Expr:
        return self.__gel_metadata__

    def __infix_op__(
        self,
        op: str,
        operand: BaseAlias | type[TypeClassProto],
        *,
        swapped: bool = False,
    ) -> Any:
        if op == "__eq__" and operand is self:
            return True

        this_operand = self.__gel_origin__
        other_operand = operand
        if isinstance(operand, BaseAlias):
            other_operand = operand.__gel_origin__

        type_class = this_operand.__gel_type_class__
        op_impl = getattr(type_class, op, None)
        if op_impl is None:
            t1 = _utils.type_repr(this_operand)
            t2 = _utils.type_repr(other_operand)
            raise TypeError(
                f"operation not supported between instances of {t1} and {t2}"
            )

        expr = op_impl(this_operand, other_operand)
        assert isinstance(expr, ExprAlias)
        metadata = expr.__gel_metadata__
        assert isinstance(metadata, BinaryOp)
        self_expr = edgeql_qb_expr(self)

        if isinstance(operand, BaseAlias):
            other_expr = assert_edgeql_qb_expr(operand)
        else:
            other_expr = metadata.lexpr if swapped else metadata.rexpr

        replacements: _BinaryOpKwargs = {}
        if swapped:
            replacements["rexpr"] = self_expr
            replacements["lexpr"] = other_expr
        else:
            replacements["lexpr"] = self_expr
            replacements["rexpr"] = other_expr

        expr.__gel_metadata__ = dataclasses.replace(metadata, **replacements)

        return expr

    def __edgeql__(self) -> tuple[type, str]:
        type_ = self.__gel_origin__
        if issubclass(type_, GelTypeMetadata):
            splat_cb = functools.partial(get_object_type_splat, type_)
        else:
            splat_cb = None
        return type_, toplevel_edgeql(self, splat_cb=splat_cb)


class PathAlias(BaseAlias):
    pass


def AnnotatedPath(origin: type, metadata: Path) -> PathAlias:  # noqa: N802
    return PathAlias(origin, metadata)


class ExprAlias(BaseAlias):
    def __bool__(self) -> bool:
        return False


def AnnotatedExpr(origin: type[Any], metadata: Expr) -> ExprAlias:  # noqa: N802
    return ExprAlias(origin, metadata)


class SortAlias(BaseAlias):
    pass


class VarAlias(BaseAlias):
    pass


def AnnotatedVar(origin: type[Any], metadata: Variable) -> VarAlias:  # noqa: N802
    return VarAlias(origin, metadata)


class GlobalAlias(BaseAlias):
    pass


def AnnotatedGlobal(origin: type[Any], metadata: Global) -> GlobalAlias:  # noqa: N802
    return GlobalAlias(origin, metadata)


def is_pointer_descriptor(v: Any) -> bool:
    return isinstance(v, (AbstractDescriptor, PathAlias)) or (
        _typing_inspect.is_annotated(v)
        and isinstance(v.__origin__, AbstractDescriptor)
    )
