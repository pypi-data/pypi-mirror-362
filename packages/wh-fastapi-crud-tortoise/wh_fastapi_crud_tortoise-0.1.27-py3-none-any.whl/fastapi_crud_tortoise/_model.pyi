from .src._settings import CRUD_DATETIME_FORMAT as CRUD_DATETIME_FORMAT
from _typeshed import Incomplete
from tortoise import Model

class CrudModel(Model):
    id: Incomplete
    created_by: Incomplete
    created_at: Incomplete
    updated_by: Incomplete
    updated_at: Incomplete
    enabled_flag: Incomplete
    trace_id: Incomplete
    async def to_dict(self, include_fields: list[str] | None = None, exclude_fields: list[str] | None = None, lc_case: bool = False): ...
    class Meta:
        abstract: bool
        table_description: str
        table_args: Incomplete

class TenantCrudModel(CrudModel):
    tenant: Incomplete
    class Meta:
        abstract: bool

class TenantModel(CrudModel):
    name: Incomplete
    description: Incomplete
    class Meta:
        table: str

class OperationsModel(TenantCrudModel):
    user: Incomplete
    action: Incomplete
    target: Incomplete
    time: Incomplete
    notes: Incomplete
    class Meta:
        table: str
