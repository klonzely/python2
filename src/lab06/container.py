# container.py
from typing import TypeVar, Generic, Callable, Optional, List, Protocol
T = TypeVar('T')

# ---------- Протоколы (задание 5) ----------
class Displayable(Protocol):
    """Объект, который можно отобразить строкой."""
    def display(self) -> str:
        ...

class Scorable(Protocol):
    """Объект, который можно оценить числом."""
    def score(self) -> float:
        ...

# ---------- TypeVar с ограничениями ----------
D = TypeVar('D', bound=Displayable)   # только объекты с методом display()
S = TypeVar('S', bound=Scorable)      # только объекты с методом score()
R = TypeVar('R')                      # для преобразования (без ограничений)

class TypedCollection(Generic[T]):
    """
    Обобщённая коллекция с методами добавления, удаления, получения,
    а также find, filter, map. Если используется с bound-протоколом,
    то внутри можно вызывать методы протокола без явного наследования.
    """
    def __init__(self) -> None:
        self._items: List[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def remove(self, item: T) -> None:
        self._items.remove(item)

    def get_all(self) -> List[T]:
        return self._items.copy()

    # ---------- Методы для задания 4 ----------
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """Возвращает первый элемент, удовлетворяющий условию, или None."""
        for item in self._items:
            if predicate(item):
                return item
        return None

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """Возвращает список всех элементов, удовлетворяющих условию."""
        return [item for item in self._items if predicate(item)]

    def map(self, transform: Callable[[T], R]) -> List[R]:
        """Применяет функцию преобразования ко всем элементам и возвращает список результатов."""
        return [transform(item) for item in self._items]

    # ---------- Дополнительные методы (вывод) ----------
    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"TypedCollection({self._items})"