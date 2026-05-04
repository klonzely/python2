from abc import ABC, abstractmethod

class Attackable(ABC):
    """Интерфейс для всего, что может атаковать."""
    @abstractmethod
    def attack(self) -> float:
        """Рассчитать урон от атаки."""
        pass

class Displayable(ABC):
    """Интерфейс для всего, что может выводить информацию о себе."""
    @abstractmethod
    def display_info(self) -> str:
        """Вернуть строковое представление объекта."""
        pass