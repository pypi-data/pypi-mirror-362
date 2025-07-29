import sqlite3

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from langgraph.store.sqlite import SqliteStore


def get_in_memory_saver() -> BaseCheckpointSaver[str]:
    """
    创建一个基于内存的检查点保存器

    Returns:
        InMemorySaver: 用于在内存中保存检查点的对象
    """
    return InMemorySaver()


def get_in_memory_store() -> BaseStore:
    """
    创建一个基于内存的存储对象

    Returns:
        InMemoryStore: 用于在内存中存储数据的对象
    """
    return InMemoryStore()


def get_sqlite_saver(db_name: str = "checkpoint.sqlite") -> BaseCheckpointSaver[str]:
    """
    创建一个基于 sqlite 的检查点保存器

    Args:
        db_name (str): 数据库名称，默认为空字符串

    Returns:
        BaseCheckpointSaver[str]: 用于在 sqlite 数据库中保存检查点的对象
    """

    return SqliteSaver(sqlite3.connect(db_name))


def get_sqlite_store(db_name: str = "store.sqlite") -> BaseStore:
    """
    创建一个基于 sqlite 的存储对象

    Args:
        db_name (str): 数据库名称，默认为空字符串

    Returns:
        BaseStore: 用于在 sqlite 数据库中存储数据的对象
    """
    return SqliteStore(sqlite3.connect(db_name))


__all__ = [
    "get_in_memory_saver",
    "get_in_memory_store",
    "get_sqlite_saver",
    "get_sqlite_store",
]
