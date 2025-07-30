from .._types import ExportColumnConfig as ExportColumnConfig, ExportConfig as ExportConfig
from io import BytesIO
from typing import Any, Callable

FormatterFunc = Callable[[Any, str], str]

def generate_excel(data: list[dict], config: ExportConfig) -> BytesIO: ...
