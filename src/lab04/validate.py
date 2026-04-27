from typing import Union, List

def validate_name(name: str) -> None:
    if not isinstance(name, str):
        raise TypeError("Название должно быть строкой")
    if not name.strip():
        raise ValueError("Название не может быть пустым")

def validate_damage(damage: Union[int, float]) -> None:
    if not isinstance(damage, (int, float)):
        raise TypeError("Урон должен быть числом")
    if damage < 0:
        raise ValueError("Урон не может быть отрицательным")

def validate_rarity(rarity: str, valid_rarities: List[str]) -> None:
    if not isinstance(rarity, str):
        raise TypeError("Редкость должна быть строкой")
    if rarity not in valid_rarities:
        raise ValueError(f"Редкость должна быть одной из: {valid_rarities}")

def validate_level(level: int, max_level: int) -> None:
    if not isinstance(level, int):
        raise TypeError("Уровень должен быть целым числом")
    if level < 1 or level > max_level:
        raise ValueError(f"Уровень должен быть от 1 до {max_level}")