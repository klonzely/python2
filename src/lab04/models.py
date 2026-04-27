from abc import ABC, abstractmethod
from interfaces import Attackable, Displayable

class Weapon(Attackable, Displayable, ABC):
    """Абстрактный базовый класс оружия."""
    
    VALID_RARITIES = ["common", "rare", "epic", "legendary"]
    MAX_LEVEL = 10

    def __init__(self, name: str, damage: float, rarity: str, level: int = 1):
        from validate import validate_name, validate_damage, validate_rarity, validate_level
        validate_name(name)
        validate_damage(damage)
        validate_rarity(rarity, self.VALID_RARITIES)
        validate_level(level, self.MAX_LEVEL)

        self._name = name.strip()
        self._damage = float(damage)
        self._rarity = rarity
        self._level = level
        self._is_broken = False

    # --- свойства ---
    @property
    def name(self) -> str: return self._name
    @property
    def damage(self) -> float: return self._damage
    @property
    def rarity(self) -> str: return self._rarity
    @property
    def level(self) -> int: return self._level
    @property
    def is_broken(self) -> bool: return self._is_broken

    @level.setter
    def level(self, new_level: int) -> None:
        if self._is_broken:
            raise ValueError("Нельзя изменить уровень сломанного оружия.")
        from validate import validate_level
        validate_level(new_level, self.MAX_LEVEL)
        self._level = new_level

    # --- бизнес-методы ---
    def upgrade(self) -> None:
        if self._is_broken:
            raise ValueError("Нельзя улучшить сломанное оружие.")
        if self._level >= self.MAX_LEVEL:
            raise ValueError("Оружие уже максимального уровня.")
        self._level += 1

    def repair(self) -> None:
        self._is_broken = False

    def break_weapon(self) -> None:
        self._is_broken = True

    # --- абстрактные методы интерфейсов ---
    @abstractmethod
    def attack(self) -> float:
        pass

    @abstractmethod
    def display_info(self) -> str:
        pass

# ---------- Конкретные классы ----------
class MeleeWeapon(Weapon):
    def __init__(self, name: str, damage: float, rarity: str, level: int = 1, sharpness: float = 1.0):
        super().__init__(name, damage, rarity, level)
        self._sharpness = sharpness

    def attack(self) -> float:
        if self._is_broken:
            return 0.0
        multiplier = {"common":1.0, "rare":1.2, "epic":1.5, "legendary":2.0}.get(self._rarity, 1.0)
        return self._damage * (1 + 0.1 * self._level) * multiplier * self._sharpness

    def display_info(self) -> str:
        status = " (сломано)" if self._is_broken else ""
        return f"🔪 Меч: {self._name} [ур.{self._level}, {self._rarity}] — урон: {self.attack():.1f}{status}"

class RangedWeapon(Weapon):
    def __init__(self, name: str, damage: float, rarity: str, level: int = 1, ammo: int = 30):
        super().__init__(name, damage, rarity, level)
        self._ammo = ammo

    def attack(self) -> float:
        if self._is_broken or self._ammo <= 0:
            return 0.0
        self._ammo -= 1
        multiplier = {"common":1.0, "rare":1.2, "epic":1.5, "legendary":2.0}.get(self._rarity, 1.0)
        return self._damage * (1 + 0.1 * self._level) * multiplier

    def reload(self, amount: int) -> None:
        self._ammo += amount

    def display_info(self) -> str:
        status = " (сломано)" if self._is_broken else ""
        return f"🏹 Лук: {self._name} [ур.{self._level}, {self._rarity}] — урон: {self.attack():.1f}, патроны: {self._ammo}{status}"