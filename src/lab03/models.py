import random
from base import Weapon

class MeleeWeapon(Weapon):
    """Оружие ближнего боя."""
    def __init__(self, name: str, damage: int, durability: int, rarity: str,
                 reach: float, material: str):
        super().__init__(name, damage, durability, rarity)
        self._reach = None
        self._material = None
        self.reach = reach
        self.material = material

    @property
    def reach(self):
        return self._reach

    @reach.setter
    def reach(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Дальность должна быть числом")
        if value < 0.5 or value > 3.0:
            raise ValueError("Дальность должна быть в диапазоне 0.5–3.0 м")
        self._reach = float(value)

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        if not isinstance(value, str):
            raise TypeError("Материал должен быть строкой")
        if value.strip() == "":
            raise ValueError("Материал не может быть пустым")
        self._material = value.strip()

    def sharpen(self):
        """Заточка: увеличивает урон на 5%, но снижает прочность на 5."""
        if self.is_broken:
            raise RuntimeError("Нельзя заточить сломанное оружие")
        self.damage = min(100, int(self.damage * 1.05))
        self.durability = max(0, self.durability - 5)

    def use(self):
        """Переопределённый метод использования: прочность падает на 15, возможен крит."""
        if self.is_broken:
            raise RuntimeError("Нельзя использовать сломанное оружие")
        # Критический урон (30% шанс) – удваивает урон для этого удара
        if random.random() < 0.3:
            print(f"Критический удар! Урон {self.damage * 2}")
        else:
            print(f"Обычный удар. Урон {self.damage}")
        # Уменьшаем прочность на 15
        new_durability = max(0, self.durability - 15)
        self.durability = new_durability

    def __str__(self):
        base_str = super().__str__()
        return (f"{base_str} | Дальность: {self._reach} м | Материал: {self._material}")

    def __repr__(self):
        return (f"MeleeWeapon(name='{self.name}', damage={self.damage}, "
                f"durability={self.durability}, rarity='{self.rarity}', "
                f"reach={self._reach}, material='{self._material}')")


class RangedWeapon(Weapon):
    """Оружие дальнего боя."""
    MAX_AMMO = 100

    def __init__(self, name: str, damage: int, durability: int, rarity: str,
                 range: int, ammo: int):
        super().__init__(name, damage, durability, rarity)
        self._range = None
        self._ammo = None
        self.range = range
        self.ammo = ammo

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, value):
        if not isinstance(value, int):
            raise TypeError("Дальность должна быть целым числом")
        if value < 10 or value > 500:
            raise ValueError("Дальность должна быть в диапазоне 10–500 м")
        self._range = value

    @property
    def ammo(self):
        return self._ammo

    @ammo.setter
    def ammo(self, value):
        if not isinstance(value, int):
            raise TypeError("Количество патронов должно быть целым")
        if value < 0 or value > RangedWeapon.MAX_AMMO:
            raise ValueError(f"Патроны должны быть в диапазоне 0–{RangedWeapon.MAX_AMMO}")
        self._ammo = value

    def reload(self, amount: int):
        """Пополнить патроны."""
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Количество для перезарядки должно быть положительным целым")
        new_ammo = min(RangedWeapon.MAX_AMMO, self._ammo + amount)
        self.ammo = new_ammo
        print(f"Перезарядка: теперь {self._ammo} патронов")

    def use(self):
        """Переопределённый метод: расходует патрон и уменьшает прочность на 5."""
        if self.is_broken:
            raise RuntimeError("Нельзя использовать сломанное оружие")
        if self._ammo == 0:
            raise RuntimeError("Нет патронов! Перезарядите оружие.")
        self._ammo -= 1
        print(f"Выстрел! Урон {self.damage}. Осталось патронов: {self._ammo}")
        # Уменьшаем прочность на 5 (меньше, чем у ближнего боя)
        new_durability = max(0, self.durability - 5)
        self.durability = new_durability

    def __str__(self):
        base_str = super().__str__()
        return (f"{base_str} | Дальность: {self._range} м | Патроны: {self._ammo}/{RangedWeapon.MAX_AMMO}")

    def __repr__(self):
        return (f"RangedWeapon(name='{self.name}', damage={self.damage}, "
                f"durability={self.durability}, rarity='{self.rarity}', "
                f"range={self._range}, ammo={self._ammo})")