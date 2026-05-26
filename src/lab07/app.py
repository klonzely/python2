from typing import List, Optional, Callable, Any
from models import Weapon, MeleeWeapon, RangedWeapon
from container import TypedCollection
from exceptions import ItemNotFoundError, DuplicateItemError
import strategies
import storage

class WeaponApp:
    """Управляет коллекцией оружия, бизнес-операциями."""
    def __init__(self, storage_file: str = "weapons.json") -> None:
        self._storage_file = storage_file
        self._collection: TypedCollection[Weapon] = TypedCollection()
        self._load_data()

    def _load_data(self) -> None:
        """Загружает данные из файла при запуске."""
        weapons = storage.load(self._storage_file)
        for w in weapons:
            self._collection.add(w)

    def save_data(self) -> None:
        """Сохраняет данные в файл."""
        storage.save(self._collection.get_all(), self._storage_file)

    def add_weapon(self, weapon: Weapon) -> None:
        """Добавляет оружие, проверяя уникальность имени."""
        existing = self._collection.find(lambda w: w.name.lower() == weapon.name.lower())
        if existing:
            raise DuplicateItemError(f"Оружие с именем '{weapon.name}' уже существует.")
        self._collection.add(weapon)

    def remove_weapon(self, name: str) -> Weapon:
        """Удаляет оружие по имени. Возвращает удалённый объект."""
        weapon = self._collection.find(lambda w: w.name.lower() == name.lower())
        if not weapon:
            raise ItemNotFoundError(f"Оружие '{name}' не найдено.")
        self._collection.remove(weapon)
        return weapon

    def find_by_name(self, name: str) -> Optional[Weapon]:
        """Поиск оружия по точному имени (без учёта регистра)."""
        return self._collection.find(lambda w: w.name.lower() == name.lower())

    def get_all(self) -> List[Weapon]:
        return self._collection.get_all()

    def filter_weapons(self, predicate: Callable[[Weapon], bool]) -> List[Weapon]:
        """Возвращает отфильтрованный список."""
        return self._collection.filter(predicate)

    def sort_weapons(self, key_func: Callable[[Weapon], Any], reverse: bool = False) -> List[Weapon]:
        """Возвращает отсортированный список (не изменяет коллекцию)."""
        return sorted(self._collection.get_all(), key=key_func, reverse=reverse)

    def apply_strategy(self, strategy: Callable[[Weapon], Weapon]) -> None:
        """Применяет стратегию ко всем элементам коллекции."""
        for w in self._collection.get_all():
            strategy(w)