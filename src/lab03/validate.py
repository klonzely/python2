def validate_name(value):
    if not isinstance(value, str):
        raise TypeError("Название должно быть строкой")
    if not value.strip():
        raise ValueError("Название не может быть пустым")
    return value.strip()

def validate_damage(value):
    if not isinstance(value, int):
        raise TypeError("Урон должен быть целым числом")
    if value < 1 or value > 100:
        raise ValueError("Урон должен быть в диапазоне 1–100")
    return value

def validate_durability(value, max_durability):
    if not isinstance(value, int):
        raise TypeError("Прочность должна быть целым числом")
    if value < 0 or value > max_durability:
        raise ValueError(f"Прочность должна быть в диапазоне 0–{max_durability}")
    return value

def validate_rarity(value):
    allowed = ("common", "rare", "epic")
    if value not in allowed:
        raise ValueError(f"Редкость должна быть одной из: {allowed}")
    return value