from .._base import CRUDGenerator as CRUDGenerator, DEPENDENCIES as DEPENDENCIES, HTTP_NOT_FOUND as HTTP_NOT_FOUND
from .._tortoise_convert import convert_to_pydantic as convert_to_pydantic
from .._types import ExportColumnConfig as ExportColumnConfig, ExportConfig as ExportConfig, FileField as FileField, IdNotExist as IdNotExist, InvalidQueryException as InvalidQueryException, MODEL_ID_TYPE as MODEL_ID_TYPE, OperationType as OperationType, PAGINATION as PAGINATION, RespModelT as RespModelT, SCHEMA as SCHEMA, TenantDataFilter as TenantDataFilter, TenantDataFilterAll as TenantDataFilterAll, TenantDataFilterTenant as TenantDataFilterTenant, TenantDataOption as TenantDataOption, UserDataFilter as UserDataFilter, UserDataFilterAll as UserDataFilterAll, UserDataFilterSelf as UserDataFilterSelf, UserDataOption as UserDataOption
from .._utils import insert_operation as insert_operation, resp_fail as resp_fail, resp_success as resp_success
from ._files import crud_savefile as crud_savefile, get_form_data as get_form_data
from ._gen_excel import generate_excel as generate_excel
from _typeshed import Incomplete
from datetime import datetime
from fastapi import File as File, Form as Form, Request as Request, UploadFile as UploadFile
from fastapi.types import IncEx as IncEx
from io import BytesIO as BytesIO
from openpyxl import Workbook as Workbook
from openpyxl.utils import get_column_letter as get_column_letter
from tortoise.models import Model
from tortoise.queryset import QuerySet as QuerySet
from typing import Any, Callable, Coroutine

CALLABLE = Callable[..., Coroutine[Any, Any, Model]]
CALLABLE_LIST = Callable[..., Coroutine[Any, Any, list[Model]]]
operator_mapping: Incomplete

def get_pk_type(schema: type[SCHEMA], pk_field: str) -> Any: ...
def parse_query(query: list[tuple[str, str, str | int | float | datetime | list[str | int | float]]], queryset: QuerySet) -> QuerySet: ...
def apply_user_tenant_filters(query: QuerySet, request: Request, user_data_filter: UserDataOption, tenant_data_filter: TenantDataOption) -> QuerySet: ...

class TortoiseCRUDRouter(CRUDGenerator[SCHEMA]):
    db_model: Incomplete
    def __init__(self, schema: type[SCHEMA], db_model: type[Model], create_schema: type[SCHEMA] | None = None, update_schema: type[SCHEMA] | None = None, filter_schema: type[SCHEMA] | None = None, user_data_option: UserDataOption = ..., tenant_data_option: TenantDataOption = ..., prefix: str | None = None, target: str | None = None, tags: list[str] | None = None, paginate: int | None = None, get_all_route: bool | DEPENDENCIES = False, get_one_route: bool | DEPENDENCIES = False, create_route: bool | DEPENDENCIES = False, update_route: bool | DEPENDENCIES = False, delete_one_route: bool | DEPENDENCIES = False, delete_all_route: bool | DEPENDENCIES = False, kcreate_route: bool | DEPENDENCIES = True, kbatch_create_route: bool | DEPENDENCIES = True, kdelete_route: bool | DEPENDENCIES = True, kbatch_delete_route: bool | DEPENDENCIES = True, kdelete_all_route: bool | DEPENDENCIES = True, kupdate_route: bool | DEPENDENCIES = True, kbatch_update_route: bool | DEPENDENCIES = True, kget_by_id_route: bool | DEPENDENCIES = True, kget_one_by_filter_route: bool | DEPENDENCIES = True, klist_route: bool | DEPENDENCIES = True, kquery_route: bool | DEPENDENCIES = True, kexport_route: bool | DEPENDENCIES = True, kquery_ex_route: bool | DEPENDENCIES = True, kupsert_route: bool | DEPENDENCIES = True, kupload_file_route: bool | DEPENDENCIES = False, kupdate_file_route: bool | DEPENDENCIES = False, **kwargs: Any) -> None: ...
    async def fun_query(self, filter, request: Request, pagination: PAGINATION, sort_by: str, relationships: bool, user_data_filter, tenant_data_filter) -> tuple[list, int, int, int]: ...
    async def create_obj_with_model(self, model, request: Request, exclude: IncEx = None, tenant_id: str = None): ...
    async def update_obj_with_model(self, obj, model, request: Request): ...
