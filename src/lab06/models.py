# models.py
from abc import abstractmethod
from typing import Union
from validate import validate_name, validate_damage, validate_rarity, validate_level

class Weapon:
    """Абстрактный базовый класс оружия (родительский)."""
    
    VALID_RARITIES = ["common", "rare", "epic", "legendary"]
    MAX_LEVEL = 10

    def __init__(self, name: str, damage: float, rarity: str, level: int = 1) -> None:
        validate_name(name)
        validate_damage(damage)
        validate_rarity(rarity, self.VALID_RARITIES)
        validate_level(level, self.MAX_LEVEL)

        self._name: str = name.strip()
        self._damage: float = float(damage)
        self._rarity: str = rarity
        self._level: int = level
        self._is_broken: bool = False

    # --- свойства ---
    @property
    def name(self) -> str:
        return self._name

    @property
    def damage(self) -> float:
        return self._damage

    @property
    def rarity(self) -> str:
        return self._rarity

    @property
    def level(self) -> int:
        return self._level

    @property
    def is_broken(self) -> bool:
        return self._is_broken

    @level.setter
    def level(self, new_level: int) -> None:
        if self._is_broken:
            raise ValueError("Нельзя изменить уровень сломанного оружия. Сначала почините его.")
        validate_level(new_level, self.MAX_LEVEL)
        self._level = new_level

    # --- бизнес-методы ---
    def upgrade(self) -> None:
        if self._is_broken:
            raise ValueError("Нельзя улучшить сломанное оружие.")
        if self._level >= self.MAX_LEVEL:
            raise ValueError(f"Оружие уже максимального уровня ({self.MAX_LEVEL}).")
        self._level += 1

    def repair(self) -> None:
        self._is_broken = False

    def break_weapon(self) -> None:
        self._is_broken = True

    # --- методы для протоколов (задание 5) ---
    def display(self) -> str:
        """Возвращает строковое описание оружия."""
        return self.display_info()

    def score(self) -> float:
        """Возвращает числовую характеристику (для сортировки, сравнения)."""
        # Например: базовый урон с поправкой на уровень
        return self._damage * (1 + 0.1 * self._level)

    @abstractmethod
    def attack(self) -> float:
        pass

    @abstractmethod
    def display_info(self) -> str:
        pass


class MeleeWeapon(Weapon):
    def __init__(self, name: str, damage: float, rarity: str, level: int = 1, sharpness: float = 1.0) -> None:
        super().__init__(name, damage, rarity, level)
        self._sharpness: float = sharpness

    def attack(self) -> float:
        if self._is_broken:
            return 0.0
        rarity_multiplier = {
            "common": 1.0,
            "rare": 1.2,
            "epic": 1.5,
            "legendary": 2.0
        }.get(self._rarity, 1.0)
        return self._damage * (1 + 0.1 * self._level) * rarity_multiplier * self._sharpness

    def display_info(self) -> str:
        status = " (сломано)" if self._is_broken else ""
        return (f"🔪 {self._name} [ур.{self._level}, {self._rarity}] — "
                f"урон: {self.attack():.1f}, острота: {self._sharpness}{status}")


class RangedWeapon(Weapon):
    def __init__(self, name: str, damage: float, rarity: str, level: int = 1, ammo: int = 30) -> None:
        super().__init__(name, damage, rarity, level)
        self._ammo: int = ammo

    def attack(self) -> float:
        if self._is_broken or self._ammo <= 0:
            return 0.0
        self._ammo -= 1
        rarity_multiplier = {
            "common": 1.0,
            "rare": 1.2,
            "epic": 1.5,
            "legendary": 2.0
        }.get(self._rarity, 1.0)
        return self._damage * (1 + 0.1 * self._level) * rarity_multiplier

    def reload(self, amount: int) -> None:
        self._ammo += amount

    def display_info(self) -> str:
        status = " (сломано)" if self._is_broken else ""
        return (f"🏹 {self._name} [ур.{self._level}, {self._rarity}] — "
                f"урон: {self.attack():.1f}, патроны: {self._ammo}{status}")