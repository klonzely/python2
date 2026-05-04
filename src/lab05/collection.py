"""
Модуль коллекции WeaponInventory с поддержкой функциональных операций.
"""

from typing import List, TypeVar, Callable, Any, Optional
from interfaces import Attackable, Displayable

T = TypeVar('T')

class WeaponInventory:
    """Коллекция оружия с методами sort_by, filter_by, apply и цепочками операций."""

    def __init__(self, items: Optional[List[T]] = None):
        self._items = list(items) if items else []

    def add(self, item: T) -> None:
        self._items.append(item)

    def get_all(self) -> List[T]:
        return self._items.copy()

    # --------------------- Базовые функциональные методы ---------------------
    def sort_by(self, key_func: Callable[[T], Any], reverse: bool = False) -> 'WeaponInventory':
        """
        Сортирует коллекцию по переданной key-функции и возвращает НОВУЮ коллекцию.
        Исходная не изменяется.
        """
        sorted_items = sorted(self._items, key=key_func, reverse=reverse)
        return WeaponInventory(sorted_items)

    def filter_by(self, predicate: Callable[[T], bool]) -> 'WeaponInventory':
        """Фильтрует коллекцию по предикату и возвращает новую коллекцию."""
        filtered_items = list(filter(predicate, self._items))
        return WeaponInventory(filtered_items)

    def apply(self, func: Callable[[T], Any]) -> 'WeaponInventory':
        """
        Применяет функцию func к каждому элементу коллекции (изменяет объекты на месте).
        Возвращает self для построения цепочек.
        """
        for item in self._items:
            func(item)
        return self

    # --------------------- Методы для демонстрации map ---------------------
    def map_to(self, transform_func: Callable[[T], Any]) -> List[Any]:
        """Применяет функцию преобразования ко всем элементам и возвращает список результатов."""
        return list(map(transform_func, self._items))

    def get_names(self) -> List[str]:
        """Вернуть список имён (демонстрация lambda)."""
        return list(map(lambda w: w.name, self._items))

    # --------------------- Дополнительные удобные методы ---------------------
    def filter_by_interface(self, interface_type) -> List[T]:
        return [item for item in self._items if isinstance(item, interface_type)]

    def print_all_displayable(self) -> None:
        for item in self.filter_by_interface(Displayable):
            print(item.display_info())

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"WeaponInventory({self._items})"