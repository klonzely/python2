from validate import validate_name, validate_damage, validate_durability, validate_rarity

class Weapon:
    MAX_DURABILITY = 100

    def __init__(self, name: str, damage: int, durability: int, rarity: str):
        self._name = None
        self._damage = None
        self._durability = None
        self._rarity = None
        self._is_broken = False

        self.name = name
        self.damage = damage
        self.durability = durability
        self.rarity = rarity

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = validate_name(value)

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = validate_damage(value)

    @property
    def durability(self):
        return self._durability

    @durability.setter
    def durability(self, value):
        new_durability = validate_durability(value, Weapon.MAX_DURABILITY)
        self._durability = new_durability
        self._is_broken = (new_durability == 0)

    @property
    def rarity(self):
        return self._rarity

    @rarity.setter
    def rarity(self, value):
        self._rarity = validate_rarity(value)

    @property
    def is_broken(self):
        return self._is_broken

    def use(self):
        """Использовать оружие: прочность падает на 10."""
        if self._is_broken:
            raise RuntimeError("Нельзя использовать сломанное оружие")
        new_durability = max(0, self._durability - 10)
        self.durability = new_durability

    def repair(self):
        """Починить оружие."""
        self.durability = Weapon.MAX_DURABILITY

    def __str__(self):
        status = "сломано" if self._is_broken else "исправно"
        return (f"{self._name} ({self._rarity}) | Урон: {self._damage} | "
                f"Прочность: {self._durability}/{Weapon.MAX_DURABILITY} | {status}")

    def __repr__(self):
        return (f"Weapon(name='{self._name}', damage={self._damage}, "
                f"durability={self._durability}, rarity='{self._rarity}')")

    def __eq__(self, other):
        if not isinstance(other, Weapon):
            return False
        return (self._name == other._name and
                self._damage == other._damage and
                self._durability == other._durability and
                self._rarity == other._rarity and
                self._is_broken == other._is_broken)