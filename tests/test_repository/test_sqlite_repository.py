from bookkeeper.repository.sqlite_repository import SQLiteRepository
from dataclasses import dataclass
import pytest

DB_NAME = 'test.db'

@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        pk: int = 0
        test_field: str = 'abc'

    return Custom


@pytest.fixture
def repo(custom_class):
    return SQLiteRepository(DB_NAME, custom_class)


def test_add_and_get(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj