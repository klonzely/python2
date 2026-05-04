"""
Демонстрация ЛР-5: функции высшего порядка, map, filter, sorted,
lambda, фабрика функций, паттерн Стратегия.
"""

from models import MeleeWeapon, RangedWeapon
from collection import WeaponInventory
from strategies import (
    by_name, by_damage, by_level, by_rarity_weight, by_total_attack_power,
    is_melee, is_ranged, is_not_broken,
    make_damage_filter,
    to_display_string, apply_discount,
    UpgradeStrategy, BreakAllStrategy
)


def main():
    print("=" * 70)
    print("Лабораторная работа №5 — Функции высшего порядка и паттерн «Стратегия»")
    print("=" * 70)

    # ---------- Создание объектов (5 штук) ----------
    sword = MeleeWeapon("Экскалибур", 20.0, "legendary", level=3, sharpness=1.5)
    bow = RangedWeapon("Длинный лук", 12.0, "rare", level=2, ammo=5)
    dagger = MeleeWeapon("Кинжал", 8.0, "common", level=1)
    axe = MeleeWeapon("Боевой топор", 18.0, "epic", level=4, sharpness=1.2)
    crossbow = RangedWeapon("Арбалет", 25.0, "rare", level=3, ammo=3)

    # Сломаем арбалет для демонстрации фильтра is_not_broken
    crossbow.break_weapon()

    collection = WeaponInventory([sword, bow, dagger, axe, crossbow])

    print("\n[Исходная коллекция]")
    collection.print_all_displayable()

    # ==================== Сценарий 1: фильтрация + сортировка + apply ====================
    print("\n" + "=" * 70)
    print("Сценарий 1: цепочка фильтр → сортировка → применение стратегии улучшения")
    print("=" * 70)

    # Фильтр: только исправное оружие, затем сортировка по урону (реальному), затем улучшить всё
    processed = (collection
                 .filter_by(is_not_broken)
                 .sort_by(by_total_attack_power, reverse=True))

    print("\n--- После фильтрации и сортировки (только исправное, по убыванию урона) ---")
    processed.print_all_displayable()

    # Применяем стратегию улучшения (callable-объект UpgradeStrategy)
    processed.apply(UpgradeStrategy())
    print("\n--- После применения UpgradeStrategy (уровень повышен на 1) ---")
    processed.print_all_displayable()

    # ==================== Сценарий 2: замена стратегии ====================
    print("\n" + "=" * 70)
    print("Сценарий 2: замена стратегии обработки (поломка вместо улучшения)")
    print("=" * 70)

    # Возьмём отдельную копию исходной коллекции (только мечи)
    swords = collection.filter_by(is_melee)
    print("\nИсходные мечи:")
    swords.print_all_displayable()

    # Применяем стратегию "сломать всё"
    swords.apply(BreakAllStrategy())
    print("\nПосле применения BreakAllStrategy (все мечи сломаны):")
    swords.print_all_displayable()

    # ==================== Сценарий 3: демонстрация callable-объекта ====================
    print("\n" + "=" * 70)
    print("Сценарий 3: явное использование callable-стратегии (UpgradeStrategy)")
    print("=" * 70)

    single_weapon = MeleeWeapon("Тестовый меч", 10.0, "common", level=1)
    print(f"До: {single_weapon.display_info()}")
    upgrade_strategy = UpgradeStrategy()
    upgrade_strategy(single_weapon)          # вызываем как функцию
    print(f"После вызова upgrade_strategy: {single_weapon.display_info()}")

    # ==================== Дополнительные демонстрации для 3 и 4 ====================
    print("\n" + "=" * 70)
    print("Дополнительные демонстрации (map, filter, lambda, фабрика)")
    print("=" * 70)

    #  map: преобразование в строки
    print("\n--- map: преобразование в строки display_info ---")
    display_strings = collection.map_to(to_display_string)
    for s in display_strings:
        print(s)

    #  filter + lambda: оружие с уроном > 10
    print("\n--- filter + lambda: оружие с базовым уроном > 10 ---")
    high_damage = list(filter(lambda w: w.damage > 10, collection.get_all()))
    for w in high_damage:
        print(w.display_info())

    #  sorted + lambda: сортировка по имени
    print("\n--- sorted + lambda: сортировка по имени (от Я до А) ---")
    sorted_by_name = sorted(collection.get_all(), key=lambda w: w.name, reverse=True)
    for w in sorted_by_name:
        print(w.display_info())

    #  Фабрика функций: фильтр по урону
    print("\n--- Фабрика make_damage_filter (урон от 10 до 20) ---")
    damage_filter = make_damage_filter(min_damage=10, max_damage=20)
    filtered_by_damage = list(filter(damage_filter, collection.get_all()))
    for w in filtered_by_damage:
        print(w.display_info())

    #  apply с lambda: повысить урон на 10%
    print("\n--- apply с lambda: повысить базовый урон на 10% у всех мечей ---")
    swords = collection.filter_by(is_melee)
    swords.apply(lambda w: setattr(w, '_damage', w.damage * 1.1))
    print("Мечи после повышения урона:")
    swords.print_all_displayable()

    #  Метод sort_by коллекции
    print("\n--- Использование collection.sort_by(by_name) ---")
    sorted_col = collection.sort_by(by_name)
    sorted_col.print_all_displayable()

    #  Метод filter_by коллекции
    print("\n--- Использование collection.filter_by(is_ranged) ---")
    ranged_col = collection.filter_by(is_ranged)
    ranged_col.print_all_displayable()


if __name__ == "__main__":
    main()