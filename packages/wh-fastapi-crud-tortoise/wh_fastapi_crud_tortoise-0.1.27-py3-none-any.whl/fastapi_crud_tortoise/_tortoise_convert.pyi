from ._types import ExtraFieldBase as ExtraFieldBase
from pydantic import BaseModel
from tortoise import Model
from typing import Literal, TypeVar

ModelType = TypeVar('ModelType', bound=Model)
PydanticType = TypeVar('PydanticType', bound=BaseModel)

def convert_to_pydantic(data: dict | ModelType | list[ModelType], pydantic_model: type[PydanticType], relationships: bool = False, mode: Literal['json', 'python'] | str = 'python') -> PydanticType | list[PydanticType]: ...
