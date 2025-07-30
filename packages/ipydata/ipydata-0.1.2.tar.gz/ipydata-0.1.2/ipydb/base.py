from abc import ABC, abstractmethod
from typing import Any, Callable, List, Type


def _delattrs(obj):
    for attr in dir(obj):
        if not attr.startswith("_"):
            delattr(obj, attr)


class BaseTable(ABC):
    def __init__(self, table: str, schema: str, global_vars: dict[str, Any]) -> None:
        self.table = table
        self.schema = schema
        self.global_vars = global_vars

        self.schema_table = f"{self.schema}.{self.table}"
        self.schema_table_copy = f"{self.schema_table}_copy"

    @abstractmethod
    def get(self): ...

    @abstractmethod
    def drop(self): ...

    def load(self):
        self.global_vars[self.table] = self.get()


class BaseSchema(ABC):
    _table_cls: Type[BaseTable]

    def __init__(self, schema: str, global_vars: dict[str, Any]) -> None:
        self._schema = schema
        self._global_vars = global_vars
        self._refresh()

    @abstractmethod
    def _list_tables(self) -> List[str]: ...

    def _add_table_attr(self, table: str):
        setattr(self, table, self._table_cls(table, self._schema, self._global_vars))

    def _refresh(self):
        _delattrs(self)
        self._tables = self._list_tables()
        for t in self._tables:
            self._add_table_attr(t)


class BaseDatabase(ABC):
    _schema_cls: Type[BaseSchema]

    def __init__(
        self,
        connection_generator: Callable,
        global_vars: dict[str, Any],
    ) -> None:
        self._connection_generator = connection_generator
        self._global_vars = global_vars
        self._refresh()

    @abstractmethod
    def _list_schemas(self) -> List[str]: ...

    def _add_schema_attr(self, schema: str):
        setattr(self, schema, self._schema_cls(schema, self._global_vars))

    def _refresh(self):
        _delattrs(self)
        self._schemas = self._list_schemas()
        for s in self._schemas:
            self._add_schema_attr(s)
