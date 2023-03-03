import sqlite3

from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T

class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        no_vals = ', '.join('?' * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({no_vals})',
                values
            )
            obj.pk = cur.lastrowid
        con.close()
        return(obj.pk)


    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            return self.db_file.get(pk)
        con.close()

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        names = list(where.keys())
        if names != []:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                cur.execute(
                    f'SELECT FROM {self.table_name} WHERE {("{param} = {where[param]} , " for param in names)} = '
                )
            con.close()
        else:
            return None


    def update(self, obj: T) -> None:
        names = list(self.fields.keys())
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            for param in names:
                cur.execute(
                    f'UPDATE {self.table_name} SET {param} = {getattr(obj, param)} WHERE rowid = {obj.pk}'
                )
        con.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'DELETE FROM {self.table_name} WHERE rowid = {obj.pk}'
            )
        con.close()

