from abc import abstractmethod
from interfaces import Attackable, Displayable
from validate import validate_name, validate_damage, validate_rarity, validate_level

class Weapon(Attackable, Displayable):
    """Абстрактный базовый класс оружия (родительский)."""
    
    VALID_RARITIES = ["common", "rare", "epic", "legendary"]
    MAX_LEVEL = 10

    def __init__(self, name: str, damage: float, rarity: str, level: int = 1):
        validate_name(name)
        validate_damage(damage)
        validate_rarity(rarity, self.VALID_RARITIES)
        validate_level(level, self.MAX_LEVEL)

        self._name = name.strip()
        self._damage = float(damage)
        self._rarity = rarity
        self._level = level
        self._is_broken = False

    # --- Свойства (геттеры) ---
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

    # --- Сеттер для уровня с валидацией и учётом состояния ---
    @level.setter
    def level(self, new_level: int) -> None:
        if self._is_broken:
            raise ValueError("Нельзя изменить уровень сломанного оружия. Сначала почините его.")
        validate_level(new_level, self.MAX_LEVEL)
        self._level = new_level

    # --- Магические методы (необязательно, но полезно) ---
    def __str__(self) -> str:
        return self.display_info()  # переиспользуем интерфейсный метод

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}(name={self._name!r}, damage={self._damage}, "
                f"rarity={self._rarity!r}, level={self._level})")

    # --- Бизнес-методы ---
    def upgrade(self) -> None:
        """Повысить уровень оружия на 1 (если не сломано и не достигнут максимум)."""
        if self._is_broken:
            raise ValueError("Нельзя улучшить сломанное оружие.")
        if self._level >= self.MAX_LEVEL:
            raise ValueError(f"Оружие уже максимального уровня ({self.MAX_LEVEL}).")
        self._level += 1

    def repair(self) -> None:
        """Починить оружие (снимает статус сломан)."""
        self._is_broken = False

    def break_weapon(self) -> None:
        """Искусственно сломать оружие (для демонстрации)."""
        self._is_broken = True

    # --- Абстрактные методы интерфейсов (должны быть переопределены в наследниках) ---
    @abstractmethod
    def attack(self) -> float:
        pass

    @abstractmethod
    def display_info(self) -> str:
        pass


class MeleeWeapon(Weapon):
    """Оружие ближнего боя (добавляет остроту)."""
    def __init__(self, name: str, damage: float, rarity: str, level: int = 1, sharpness: float = 1.0):
        super().__init__(name, damage, rarity, level)
        self._sharpness = sharpness

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
    """Оружие дальнего боя (добавляет боеприпасы)."""
    def __init__(self, name: str, damage: float, rarity: str, level: int = 1, ammo: int = 30):
        super().__init__(name, damage, rarity, level)
        self._ammo = ammo

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
        """Пополнить боеприпасы."""
        self._ammo += amount

    def display_info(self) -> str:
        status = " (сломано)" if self._is_broken else ""
        return (f"🏹 {self._name} [ур.{self._level}, {self._rarity}] — "
                f"урон: {self.attack():.1f}, патроны: {self._ammo}{status}")