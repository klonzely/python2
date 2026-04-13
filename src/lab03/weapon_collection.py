from typing import List, Callable, Union
from base import Weapon

class WeaponCollection:
    def __init__(self):
        self._items: List[Weapon] = []

    def _validate_type(self, item):
        if not isinstance(item, Weapon):
            raise TypeError(f"Ожидается Weapon, получен {type(item).__name__}")

    def _is_duplicate(self, item) -> bool:
        for w in self._items:
            if (w.name == item.name and
                w.damage == item.damage and
                w.durability == item.durability and
                w.rarity == item.rarity and
                w.is_broken == item.is_broken):
                return True
        return False

    def add(self, item: Weapon):
        self._validate_type(item)
        if self._is_duplicate(item):
            raise ValueError("Такое оружие уже есть в коллекции")
        self._items.append(item)

    def remove(self, item: Weapon):
        self._validate_type(item)
        if item in self._items:
            self._items.remove(item)
        else:
            raise ValueError("Оружие не найдено в коллекции")

    def get_all(self) -> List[Weapon]:
        return self._items.copy()

    def find_by_name(self, name: str) -> List[Weapon]:
        return [w for w in self._items if w.name == name]

    def find_by_damage(self, damage: int) -> List[Weapon]:
        return [w for w in self._items if w.damage == damage]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index: int) -> Weapon:
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        return self._items[index]

    def remove_at(self, index: int):
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        del self._items[index]

    def sort(self, key: Union[str, Callable] = 'damage', reverse: bool = False):
        allowed_keys = ['name', 'damage', 'durability', 'rarity']
        if isinstance(key, str):
            if key not in allowed_keys:
                raise ValueError(f"Недопустимый ключ: {key}. Допустимые: {allowed_keys}")
            self._items.sort(key=lambda w: getattr(w, key), reverse=reverse)
        else:
            self._items.sort(key=key, reverse=reverse)

    def filter(self, condition: Callable[[Weapon], bool]) -> 'WeaponCollection':
        new_coll = WeaponCollection()
        for w in self._items:
            if condition(w):
                new_coll.add(w)
        return new_coll

    def get_broken(self) -> 'WeaponCollection':
        return self.filter(lambda w: w.is_broken)

    def get_by_min_damage(self, min_damage: int) -> 'WeaponCollection':
        return self.filter(lambda w: w.damage >= min_damage)