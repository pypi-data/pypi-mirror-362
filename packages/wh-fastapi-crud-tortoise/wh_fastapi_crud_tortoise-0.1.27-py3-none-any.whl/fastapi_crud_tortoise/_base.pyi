import abc
from ._types import RespModelT as RespModelT, SCHEMA as SCHEMA, TenantDataFilter as TenantDataFilter, TenantDataFilterAll as TenantDataFilterAll, TenantDataFilterTenant as TenantDataFilterTenant, TenantDataOption as TenantDataOption, UserDataFilter as UserDataFilter, UserDataFilterAll as UserDataFilterAll, UserDataFilterSelf as UserDataFilterSelf, UserDataOption as UserDataOption
from ._utils import pagination_factory as pagination_factory, schema_factory as schema_factory
from _typeshed import Incomplete
from abc import ABC
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.types import DecoratedCallable as DecoratedCallable
from typing import Any, Callable, Generic, Sequence

DEPENDENCIES = Sequence[Depends] | None
HTTP_NOT_FOUND: Incomplete

class IOrmImpl(ABC, metaclass=abc.ABCMeta): ...

class CRUDGenerator(APIRouter, IOrmImpl, Generic[SCHEMA], metaclass=abc.ABCMeta):
    schema: Incomplete
    pagination: Incomplete
    create_schema: Incomplete
    update_schema: Incomplete
    batch_update_schema: Incomplete
    filter_schema: Incomplete
    target: Incomplete
    user_data_filter_type: Incomplete
    user_data_filter_defv: Incomplete
    tenant_data_filter_type: Incomplete
    tenant_data_filter_defv: Incomplete
    def __init__(self, schema: type[SCHEMA], create_schema: type[SCHEMA] | None = None, update_schema: type[SCHEMA] | None = None, filter_schema: type[SCHEMA] | None = None, user_data_option: UserDataOption = ..., tenant_data_option: TenantDataOption = ..., prefix: str | None = None, target: str | None = None, tags: list[str] | None = None, paginate: int | None = None, get_all_route: bool | DEPENDENCIES = True, get_one_route: bool | DEPENDENCIES = True, create_route: bool | DEPENDENCIES = True, update_route: bool | DEPENDENCIES = True, delete_one_route: bool | DEPENDENCIES = True, delete_all_route: bool | DEPENDENCIES = True, kcreate_route: bool | DEPENDENCIES = True, kbatch_create_route: bool | DEPENDENCIES = True, kdelete_route: bool | DEPENDENCIES = True, kbatch_delete_route: bool | DEPENDENCIES = True, kdelete_all_route: bool | DEPENDENCIES = True, kupdate_route: bool | DEPENDENCIES = True, kbatch_update_route: bool | DEPENDENCIES = True, kget_by_id_route: bool | DEPENDENCIES = True, kget_one_by_filter_route: bool | DEPENDENCIES = True, klist_route: bool | DEPENDENCIES = True, kquery_route: bool | DEPENDENCIES = True, kexport_route: bool | DEPENDENCIES = True, kquery_ex_route: bool | DEPENDENCIES = True, kupsert_route: bool | DEPENDENCIES = True, kupload_file_route: bool | DEPENDENCIES = True, kupdate_file_route: bool | DEPENDENCIES = True, **kwargs: Any) -> None: ...
    def api_route(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]: ...
    def get(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]: ...
    def post(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]: ...
    def put(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]: ...
    def delete(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]: ...
    def remove_api_route(self, path: str, methods: list[str]) -> None: ...
