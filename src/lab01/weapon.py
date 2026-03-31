# weapon.py
from validate import validate_name, validate_damage, validate_rarity, validate_level

class Weapon:
    """Класс оружия с уровнем, редкостью и состоянием целостности."""
    
    # Атрибуты класса
    VALID_RARITIES = ["common", "rare", "epic", "legendary"]
    MAX_LEVEL = 10

    def __init__(self, name: str, damage: float, rarity: str, level: int = 1):
        """
        Конструктор оружия.
        :param name: название (не пустое)
        :param damage: базовый урон (>= 0)
        :param rarity: редкость (common, rare, epic, legendary)
        :param level: уровень (1..MAX_LEVEL)
        """
        # Валидация входных данных
        validate_name(name)
        validate_damage(damage)
        validate_rarity(rarity, self.VALID_RARITIES)
        validate_level(level, self.MAX_LEVEL)

        self._name = name.strip()
        self._damage = float(damage)
        self._rarity = rarity
        self._level = level
        self._is_broken = False  # состояние: сломано/не сломано

    # region Свойства (геттеры)
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
    # endregion

    # region Сеттер (с валидацией и учётом состояния)
    @level.setter
    def level(self, new_level: int) -> None:
        """
        Сеттер для уровня. Проверяет:
        - корректен ли новый уровень (тип, диапазон)
        - не сломано ли оружие (нельзя менять уровень сломанного оружия)
        """
        if self._is_broken:
            raise ValueError("Нельзя изменить уровень сломанного оружия. Сначала почините его.")
        validate_level(new_level, self.MAX_LEVEL)
        self._level = new_level
    # endregion

    # region Магические методы
    def __str__(self) -> str:
        """Красивый вывод для пользователя."""
        status = " (сломано)" if self._is_broken else ""
        return (f"{self._name} [ур. {self._level}, {self._rarity}]"
                f" – урон: {self._damage:.1f}{status}")

    def __repr__(self) -> str:
        """Техническое представление."""
        return (f"Weapon(name={self._name!r}, damage={self._damage}, "
                f"rarity={self._rarity!r}, level={self._level})")

    def __eq__(self, other: object) -> bool:
        """Два оружия считаются равными, если у них совпадают имя, урон, редкость и уровень."""
        if not isinstance(other, Weapon):
            return False
        return (self._name == other._name and
                self._damage == other._damage and
                self._rarity == other._rarity and
                self._level == other._level)
    # endregion

    # region Бизнес-методы
    def upgrade(self) -> None:
        """
        Повысить уровень оружия на 1.
        Проверяет, не сломано ли оружие и не достигнут ли максимум.
        """
        if self._is_broken:
            raise ValueError("Нельзя улучшить сломанное оружие.")
        if self._level >= self.MAX_LEVEL:
            raise ValueError(f"Оружие уже максимального уровня ({self.MAX_LEVEL}).")
        self._level += 1

    def repair(self) -> None:
        """Починить оружие (снимает статус сломан)."""
        self._is_broken = False

    def attack(self) -> float:
        """
        Рассчитать итоговый урон в зависимости от уровня и редкости.
        Если оружие сломано – урон равен 0.
        Формула: урон * (1 + 0.1 * уровень) * множитель редкости.
        Множители: common = 1.0, rare = 1.2, epic = 1.5, legendary = 2.0
        """
        if self._is_broken:
            return 0.0

        rarity_multiplier = {
            "common": 1.0,
            "rare": 1.2,
            "epic": 1.5,
            "legendary": 2.0
        }.get(self._rarity, 1.0)

        return self._damage * (1 + 0.1 * self._level) * rarity_multiplier

    def break_weapon(self) -> None:
        """Искусственно сломать оружие (для демонстрации состояний)."""
        self._is_broken = True
    # endregion