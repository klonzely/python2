"""
Модуль с функциями-стратегиями для сортировки, фильтрации,
преобразования и обработки объектов оружия.
"""

from typing import Callable, Any

# ---------- Стратегии сортировки (key-функции) ----------
def by_name(weapon) -> str:
    """Ключ сортировки по имени."""
    return weapon.name

def by_damage(weapon) -> float:
    """Ключ сортировки по базовому урону."""
    return weapon.damage

def by_level(weapon) -> int:
    """Ключ сортировки по уровню."""
    return weapon.level

def by_rarity_weight(weapon) -> int:
    """Ключ сортировки по весу редкости (числовой эквивалент)."""
    rarity_order = {"common": 1, "rare": 2, "epic": 3, "legendary": 4}
    return rarity_order.get(weapon.rarity, 0)

def by_total_attack_power(weapon) -> float:
    """
    Ключ сортировки по реальному урону (с учётом редкости, уровня и состояния).
    Вызывает attack(), что для сломанного оружия даст 0.
    """
    return weapon.attack()

# ---------- Функции-фильтры (предикаты) ----------
def is_melee(weapon) -> bool:
    """Фильтр: только ближнее оружие (MeleeWeapon)."""
    from models import MeleeWeapon
    return isinstance(weapon, MeleeWeapon)

def is_ranged(weapon) -> bool:
    """Фильтр: только дальнее оружие (RangedWeapon)."""
    from models import RangedWeapon
    return isinstance(weapon, RangedWeapon)

def is_not_broken(weapon) -> bool:
    """Фильтр: только исправное оружие."""
    return not weapon.is_broken

# ---------- Фабрика функций-фильтров (замыкание) ----------
def make_damage_filter(min_damage: float = 0, max_damage: float = float('inf')):
    """
    Создаёт фильтр, который пропускает оружие с базовым уроном в диапазоне [min_damage, max_damage].
    """
    def filter_by_damage(weapon) -> bool:
        return min_damage <= weapon.damage <= max_damage
    return filter_by_damage

# ---------- Функции для map (преобразование) ----------
def to_display_string(weapon) -> str:
    """Преобразует оружие в строку через display_info() (интерфейс Displayable)."""
    return weapon.display_info()

def apply_discount(percent: float) -> Callable:
    """
    Фабрика: создаёт функцию для снижения базового урона на заданный процент.
    Изменяет объект (мутирует) – используется в apply().
    """
    def discount(weapon):
        weapon._damage = weapon.damage * (1 - percent / 100)
        return weapon
    return discount

# ---------- Callable-объект для паттерна «Стратегия» ----------
class UpgradeStrategy:
    """Стратегия улучшения оружия (повышение уровня)."""
    def __call__(self, weapon):
        try:
            weapon.upgrade()
        except ValueError as e:
            print(f"Не удалось улучшить {weapon.name}: {e}")
        return weapon

class BreakAllStrategy:
    """Стратегия: поломать всё оружие (для демонстрации)."""
    def __call__(self, weapon):
        weapon.break_weapon()
        return weapon