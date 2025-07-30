import typing
from typing import TYPE_CHECKING, overload, Any, Optional, Union, AsyncContextManager

from sqlalchemy import (
    CompoundSelect,
    CursorResult,
    Executable,
    Select,
    UpdateBase,
    util,
)
from sqlalchemy import ScalarSelect, SelectBase
from sqlalchemy.engine import Result
from sqlalchemy.engine.interfaces import (
    _CoreAnyExecuteParams,  # type: ignore[reportPrivateUsage]
)
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, AsyncSessionTransaction
from sqlalchemy.orm._typing import (
    OrmExecuteOptionsParameter,  # type: ignore[reportPrivateUsage]
)
from sqlalchemy.sql.selectable import TypedReturnsRows

from .types import Insert, Select, Update, Delete, Exists, CompoundSelect, postgresql

if TYPE_CHECKING:
    # noinspection PyProtectedMember
    from sqlalchemy.sql._typing import _ColumnsClauseArgument, _DMLTableArgument, _SelectStatementForCompoundArgument
    # noinspection PyProtectedMember
    from sqlalchemy.sql._typing import (
        _TypedColumnClauseArgument,
        _ColumnsClauseArgument,
        _T0, _T1, _T2, _T3,
        _T4, _T5, _T6, _T7,
        _T8, _T9
    )

_T = typing.TypeVar("_T", covariant=True, bound=Any)


class PostgreSQL:
    def insert(self, table: _DMLTableArgument) -> postgresql.Insert: ...


class SQLAlchemyTransactionContext:
    engine: AsyncEngine
    postgresql: PostgreSQL

    def __init__(
        self,
        engine: AsyncEngine,
        default_session_maker: typing.Callable[
            [], typing.AsyncContextManager[AsyncSession]
        ] = None
    ): ...

    def transaction(
        self,
        session_maker=None
    ) -> AsyncContextManager[Union[AsyncSession, AsyncSessionTransaction]]: ...

    def current_transaction_or_default(self) -> AsyncContextManager[AsyncSession]: ...

    def get_current_transaction(self) -> Optional[AsyncSession]: ...

    async def new_transaction(
        self,
        session_maker=None
    ) -> AsyncContextManager[Union[AsyncSession, AsyncSessionTransaction]]: ...

    @overload
    def select(self, __ent0: _TypedColumnClauseArgument[_T0]) -> Select[_T0]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1]
    ) -> Select[Union[_T0, _T1]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2]
    ) -> Select[Union[_T0, _T1, _T2]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
    ) -> Select[Union[_T0, _T1, _T2, _T3]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
        __ent5: _TypedColumnClauseArgument[_T5],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4, _T5]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
        __ent5: _TypedColumnClauseArgument[_T5],
        __ent6: _TypedColumnClauseArgument[_T6],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
        __ent5: _TypedColumnClauseArgument[_T5],
        __ent6: _TypedColumnClauseArgument[_T6],
        __ent7: _TypedColumnClauseArgument[_T7],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
        __ent5: _TypedColumnClauseArgument[_T5],
        __ent6: _TypedColumnClauseArgument[_T6],
        __ent7: _TypedColumnClauseArgument[_T7],
        __ent8: _TypedColumnClauseArgument[_T8],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8]]: ...


    @overload
    def select(
        self,
        __ent0: _TypedColumnClauseArgument[_T0],
        __ent1: _TypedColumnClauseArgument[_T1],
        __ent2: _TypedColumnClauseArgument[_T2],
        __ent3: _TypedColumnClauseArgument[_T3],
        __ent4: _TypedColumnClauseArgument[_T4],
        __ent5: _TypedColumnClauseArgument[_T5],
        __ent6: _TypedColumnClauseArgument[_T6],
        __ent7: _TypedColumnClauseArgument[_T7],
        __ent8: _TypedColumnClauseArgument[_T8],
        __ent9: _TypedColumnClauseArgument[_T9],
    ) -> Select[Union[_T0, _T1, _T2, _T3, _T4, _T5, _T6, _T7, _T8, _T9]]: ...


    # END OVERLOADED FUNCTIONS select


    @overload
    def select(
        self,
        *entities: _ColumnsClauseArgument[Any], **__kw: Any
    ) -> Select[Any]: ...

    def select(self, *entities: _ColumnsClauseArgument[Any], **__kw: Any) -> Select[Any]: ...


    def insert(self, table: _DMLTableArgument) -> Insert: ...


    def update(self, table: _DMLTableArgument) -> Update: ...

    def delete(self, table: _DMLTableArgument) -> Delete: ...

    def union(self, *selects: _SelectStatementForCompoundArgument) -> CompoundSelect: ...

    def union_all(self, *selects: _SelectStatementForCompoundArgument) -> CompoundSelect: ...

    def exists(
        self, __argument: Optional[Union[_ColumnsClauseArgument[Any], SelectBase, ScalarSelect[Any]]] = None
    ) -> Exists: ...

    @overload
    async def execute(
        self,
        statement: TypedReturnsRows[_T],
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[dict[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
    ) -> Result[_T]: ...

    @overload
    async def execute(
        self,
        statement: UpdateBase,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[dict[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
    ) -> CursorResult[Any]: ...

    @overload
    async def execute(
        self,
        statement: Executable,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[dict[str, Any]] = None,
        _parent_execute_state: Optional[Any] = None,
        _add_event: Optional[Any] = None,
    ) -> Result[Any]: ...

    async def execute(
        self,
        statement: Executable,
        params: Optional[_CoreAnyExecuteParams] = None,
        *,
        execution_options: OrmExecuteOptionsParameter = util.EMPTY_DICT,
        bind_arguments: Optional[dict[str, Any]] = None,
        **kw: Any,
    ) -> Result[Any]: ...
