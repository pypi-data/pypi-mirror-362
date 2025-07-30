from _typeshed import Incomplete
from datetime import date as date, datetime as datetime
from enum import Enum
from fastapi.responses import ORJSONResponse as ORJSONResponse
from pydantic import BaseModel
from typing import Generic, TypeVar
from uuid import UUID

PAGINATION = dict[str, int | None]
PGProtoUUID: Incomplete
UUIDTypes: Incomplete
UUIDTypes = UUID

def convert_uuid(v: any) -> str: ...

MODEL_ID_TYPE: Incomplete

class UserDataFilter(str, Enum):
    ALL_DATA = 'ALL_DATA'
    SELF_DATA = 'SELF_DATA'

class UserDataFilterAll(str, Enum):
    ALL_DATA = 'ALL_DATA'

class UserDataFilterSelf(str, Enum):
    SELF_DATA = 'SELF_DATA'

class UserDataOption(str, Enum):
    ALL_ONLY = 'ALL_ONLY'
    ALL_DEFAULT = 'ALL_DEFAULT'
    SELF_ONLY = 'SELF_ONLY'
    SELF_DEFAULT = 'SELF_DEFAULT'

class TenantDataFilter(str, Enum):
    ALL_DATA = 'ALL_DATA'
    TENANT_DATA = 'TENANT_DATA'

class TenantDataFilterAll(str, Enum):
    ALL_DATA = 'ALL_DATA'

class TenantDataFilterTenant(str, Enum):
    TENANT_DATA = 'TENANT_DATA'

class TenantDataOption(str, Enum):
    ALL_ONLY = 'ALL_ONLY'
    ALL_DEFAULT = 'ALL_DEFAULT'
    TENANT_ONLY = 'TENANT_ONLY'
    TENANT_DEFAULT = 'TENANT_DEFAULT'

class OperationType(str, Enum):
    LOGIN = 'LOGIN'
    LOGOUT = 'LOGOUT'
    ADD = 'ADD'
    DELETE = 'DELETE'
    EDIT = 'EDIT'
    ENABLE = 'ENABLE'
    DISABLE = 'DISABLE'
    UPLOAD = 'UPLOAD'
    EXPORT = 'EXPORT'
    IMPORT = 'IMPORT'
    BIND = 'BIND'
    REBIND = 'REBIND'
    SEND = 'SEND'
    BATCH_SET = 'BATCH_SET'
SCHEMA = TypeVar('SCHEMA', bound=BaseModel)

class ExtraFieldBase(BaseModel): ...

FileField: Incomplete
RespT = TypeVar('RespT', bound=BaseModel | list[BaseModel] | int | bool | str)

class RespModelT(BaseModel, Generic[RespT]):
    code: int
    msg: str
    data: RespT | None
    success: bool
    trace_id: str | None

class IdNotExist(Exception):
    def __init__(self) -> None: ...

class InvalidQueryException(Exception):
    def __init__(self, msg: str = 'invalid query') -> None: ...
FILTER_SCHEMA = TypeVar('FILTER_SCHEMA')

class ExportColumnConfig(BaseModel):
    name: str
    field: str
    default: str | None
    formatter: str | None

class ExportConfig(BaseModel, Generic[FILTER_SCHEMA]):
    filter: FILTER_SCHEMA | None
    columns: list[ExportColumnConfig]
    filename: str
    sheet_name: str
    include_null: bool
