from typing import List, TypeVar, Generic, Callable
from interfaces import Attackable, Displayable

T = TypeVar('T')

class WeaponInventory(Generic[T]):
    """Коллекция, работающая с объектами через интерфейсы."""
    def __init__(self):
        self._items: List[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def get_all(self) -> List[T]:
        return self._items.copy()

    def filter_by_interface(self, interface_type) -> List:
        """Возвращает все объекты, реализующие переданный интерфейс."""
        return [item for item in self._items if isinstance(item, interface_type)]

    def sort_by_attack(self) -> List[Attackable]:
        """Сортирует по урону (только объекты, реализующие Attackable)."""
        attackable = self.filter_by_interface(Attackable)
        return sorted(attackable, key=lambda x: x.attack(), reverse=True)

    def print_all_displayable(self) -> None:
        """Выводит информацию всех Displayable-объектов."""
        for item in self.filter_by_interface(Displayable):
            print(item.display_info())