import json
from typing import List
from models import Weapon

def save(collection: List[Weapon], filepath: str) -> None:
    """Сохраняет список оружия в JSON-файл."""
    data = [w.to_dict() for w in collection]
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load(filepath: str) -> List[Weapon]:
    """Загружает список оружия из JSON-файла. Если файла нет, возвращает пустой список."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        weapons = []
        for item in data:
            weapons.append(Weapon.from_dict(item))
        return weapons
    except FileNotFoundError:
        return []