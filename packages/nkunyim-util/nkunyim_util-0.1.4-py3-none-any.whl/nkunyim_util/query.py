from datetime import datetime
from decimal import Decimal
from typing import Callable, Optional, Union
from uuid import UUID

from nkunyim_util.command import is_uuid


def parse_value(value: str, typ: str) -> Optional[object]:
    type_parsers: dict[str, Callable[[str], object]] = {
        'uuid': lambda v: UUID(v) if is_uuid(v) else None,
        'bool': lambda v: str(v).lower() in {'true', '1'},
        'str': str,
        'int': int,
        'float': float,
        'decimal': Decimal,
        'date': lambda v: datetime.strptime(v, '%Y-%m-%d %H:%M:%S').date(),
        'time': lambda v: datetime.strptime(v, '%Y-%m-%d %H:%M:%S').time(),
        'timez': lambda v: datetime.strptime(v, '%Y-%m-%d %H:%M:%S').timestamp(),
        'datetime': lambda v: datetime.strptime(v, '%Y-%m-%d %H:%M:%S'),
    }

    parser = type_parsers.get(typ)
    if not parser:
        return value  # Fallback to raw string if type is unknown

    try:
        return parser(value)
    except Exception:
        return None  # Optional: add logging here if needed


class Query:
    def __init__(self) -> None:
        self.params = {}

    def _build(self, key: str, typ: str, val: str) -> None:
        parsed = parse_value(val, typ)
        if parsed is not None:
            self.params[key] = parsed

    def extract(self, schema: Optional[dict[str, str]] = None, query_params: Optional[dict[str, str]] = None) -> None:
        query_params = query_params or {}
        schema = schema or {}

        for key, typ in schema.items():
            if key in query_params:
                self._build(key, typ, query_params[key])
