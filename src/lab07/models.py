from abc import abstractmethod
from typing import Union
from validate import validate_name, validate_damage, validate_rarity, validate_level

class Weapon:
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
            raise ValueError("Нельзя изменить уровень сломанного оружия.")
        validate_level(new_level, self.MAX_LEVEL)
        self._level = new_level

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

    def display(self) -> str:
        return self.display_info()

    def score(self) -> float:
        # Базовый показатель для сортировки
        return self._damage * (1 + 0.1 * self._level)

    @abstractmethod
    def attack(self) -> float:
        pass

    @abstractmethod
    def display_info(self) -> str:
        pass

    def to_dict(self) -> dict:
        """Сериализация в словарь для JSON."""
        return {
            "type": self.__class__.__name__,
            "name": self._name,
            "damage": self._damage,
            "rarity": self._rarity,
            "level": self._level,
            "is_broken": self._is_broken,
            "sharpness": getattr(self, "_sharpness", None),
            "ammo": getattr(self, "_ammo", None),
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Десериализация из словаря."""
        typ = data["type"]
        if typ == "MeleeWeapon":
            return MeleeWeapon(
                name=data["name"],
                damage=data["damage"],
                rarity=data["rarity"],
                level=data["level"],
                sharpness=data.get("sharpness", 1.0)
            )
        elif typ == "RangedWeapon":
            w = RangedWeapon(
                name=data["name"],
                damage=data["damage"],
                rarity=data["rarity"],
                level=data["level"],
                ammo=data.get("ammo", 30)
            )
            if data.get("is_broken"):
                w.break_weapon()
            return w
        else:
            raise ValueError(f"Неизвестный тип оружия: {typ}")

class MeleeWeapon(Weapon):
    def __init__(self, name: str, damage: float, rarity: str, level: int = 1, sharpness: float = 1.0) -> None:
        super().__init__(name, damage, rarity, level)
        self._sharpness: float = sharpness

    def attack(self) -> float:
        if self._is_broken:
            return 0.0
        mult = {"common":1.0, "rare":1.2, "epic":1.5, "legendary":2.0}.get(self._rarity, 1.0)
        return self._damage * (1 + 0.1 * self._level) * mult * self._sharpness

    def display_info(self) -> str:
        status = " (сломано)" if self._is_broken else ""
        return f"🔪 {self._name} [ур.{self._level}, {self._rarity}] — урон: {self.attack():.1f}, острота: {self._sharpness}{status}"

class RangedWeapon(Weapon):
    def __init__(self, name: str, damage: float, rarity: str, level: int = 1, ammo: int = 30) -> None:
        super().__init__(name, damage, rarity, level)
        self._ammo: int = ammo

    def attack(self) -> float:
        if self._is_broken or self._ammo <= 0:
            return 0.0
        self._ammo -= 1
        mult = {"common":1.0, "rare":1.2, "epic":1.5, "legendary":2.0}.get(self._rarity, 1.0)
        return self._damage * (1 + 0.1 * self._level) * mult

    def reload(self, amount: int) -> None:
        self._ammo += amount

    def display_info(self) -> str:
        status = " (сломано)" if self._is_broken else ""
        return f"🏹 {self._name} [ур.{self._level}, {self._rarity}] — урон: {self.attack():.1f}, патроны: {self._ammo}{status}"