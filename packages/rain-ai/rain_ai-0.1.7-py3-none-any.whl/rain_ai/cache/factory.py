from typing import Literal, Any

from cachetools import Cache

from rain_ai.cache.create import (
    create_cache,
    create_lru_cache,
    create_lfu_cache,
    create_ttl_cache,
    create_rr_cache,
    create_fifo_cache,
)
from rain_ai.cache.operation import (
    has_key_in_cache,
    get_value_from_cache,
    add_value_to_cache,
    update_value_in_cache,
    remove_key_from_cache,
    get_items_of_cache,
    get_keys_of_cache,
    get_values_of_cache,
    get_max_size_of_cache,
    get_current_size_of_cache,
)


class CACHE:
    def __init__(
        self,
        cache_type: Literal["basic", "lru", "lfu", "ttl", "rr", "fifo"],
        maxsize: int,
        ttl: int | None,
    ) -> None:
        """
        创建一个缓存实例

        Args:
            cache_type (Literal["basic", "lru", "lfu", "ttl", "rr", "fifo"]): 缓存类型
                - basic: 基础缓存
                - lru: 最近最少使用缓存
                - lfu: 最少使用缓存
                - ttl: 有效时间缓存
                - rr: 轮询缓存
                - fifo: 先进先出缓存
            maxsize (int): 缓存的最大大小，默认为20
            ttl (int | None): 缓存的有效时间，单位为秒，默认为None表示无限制，仅在cache_type为ttl时有效

        """
        self.cache_type = cache_type
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = self._create_cache()

    def _create_cache(self) -> Cache:
        """
        创建缓存实例

        Returns:
            Cache: 缓存实例

        """
        if self.cache_type == "basic":
            return create_cache(maxsize=self.maxsize)
        elif self.cache_type == "lru":
            return create_lru_cache(maxsize=self.maxsize)
        elif self.cache_type == "lfu":
            return create_lfu_cache(maxsize=self.maxsize)
        elif self.cache_type == "ttl":
            return create_ttl_cache(maxsize=self.maxsize, ttl=self.ttl)
        elif self.cache_type == "rr":
            return create_rr_cache(maxsize=self.maxsize)
        elif self.cache_type == "fifo":
            return create_fifo_cache(maxsize=self.maxsize)
        else:
            raise ValueError(f"Unsupported cache type: {self.cache_type}")

    def has(self, key: str) -> bool:
        """
        检查缓存中是否存在指定的键

        Args:
            key (str): 要检查的键

        Returns:
            bool: 如果键存在于缓存中，则返回True，否则返回False

        """
        return has_key_in_cache(self.cache, key)

    def max_size(self) -> float:
        """
        获取缓存的最大大小

        Returns:
            float: 缓存的最大大小

        """
        return get_max_size_of_cache(self.cache)

    def current_size(self) -> float:
        """
        获取缓存的当前大小

        Returns:
            float: 缓存的当前大小

        """
        return get_current_size_of_cache(self.cache)

    def keys(self) -> list:
        """
        获取缓存中所有的键

        Returns:
            list: 缓存中所有的键

        """
        return get_keys_of_cache(self.cache)

    def values(self) -> list:
        """
        获取缓存中所有的值

        Returns:
            list: 缓存中所有的值

        """
        return get_values_of_cache(self.cache)

    def items(self) -> list:
        """
        获取缓存中所有的键值对

        Returns:
            list: 缓存中所有的键值对

        """
        return get_items_of_cache(self.cache)

    def get(self, key: str) -> Any:
        """
        从缓存中获取指定键的值

        Args:
            key (str): 要获取的键

        Returns:
            Any: 如果键存在于缓存中，则返回对应的值，否则返回None

        """
        return get_value_from_cache(self.cache, key)

    def add(self, key: str, value: Any) -> None:
        """
        向缓存中添加一个键值对

        Args:
            key (str): 要添加的键
            value (Any): 要添加的值

        """
        add_value_to_cache(self.cache, key, value)

    def update(self, key: str, value: Any) -> None:
        """
        更新缓存中指定键的值

        Args:
            key (str): 要更新的键
            value (Any): 要更新的值

        """
        update_value_in_cache(self.cache, key, value)

    def remove(self, key: str) -> None:
        """
        从缓存中移除指定的键

        Args:
            key (str): 要移除的键

        """
        remove_key_from_cache(self.cache, key)


def cache_factory(
    cache_type: Literal["basic", "lru", "lfu", "ttl", "rr", "fifo"] = "lru",
    maxsize: int = 20,
    ttl: int | None = None,
) -> CACHE:
    """
    创建一个缓存实例

    Args:
        cache_type (Literal["basic", "lru", "lfu", "ttl", "rr", "fifo"]): 缓存类型
            - basic: 基础缓存
            - lru: 最近最少使用缓存
            - lfu: 最少使用缓存
            - ttl: 有效时间缓存
            - rr: 轮询缓存
            - fifo: 先进先出缓存
        maxsize (int): 缓存的最大大小，默认为20
        ttl (int | None): 缓存的有效时间，单位为秒，默认为None表示无限制，仅在cache_type为ttl时有效
    Returns:
        Cache: 缓存实例
    """
    return CACHE(cache_type, maxsize, ttl)


__all__ = ["cache_factory"]
