from base import Weapon
from models import MeleeWeapon, RangedWeapon
from weapon_collection import WeaponCollection   # ← теперь локальная версия

def filter_by_type(collection, cls):
    new_coll = WeaponCollection()
    for item in collection:
        if isinstance(item, cls):
            new_coll.add(item)
    return new_coll

def get_melee(collection):
    return filter_by_type(collection, MeleeWeapon)

def get_ranged(collection):
    return filter_by_type(collection, RangedWeapon)

def main():
    print("=== Лабораторная работа №3: Наследование и полиморфизм ===\n")

    # ----- Сценарий 1 (оценка 3) -----
    print("--- Сценарий 1: Создание объектов и методы ---")
    sword = MeleeWeapon("Экскалибур", 45, 100, "epic", reach=1.2, material="сталь")
    bow = RangedWeapon("Длинный лук", 30, 100, "rare", range=150, ammo=20)

    print(sword)
    print(bow)

    print("\nИспользуем меч (обычный use):")
    sword.use()
    print(sword)

    print("\nЗатачиваем меч:")
    sword.sharpen()
    print(sword)

    print("\nИспользуем лук:")
    bow.use()
    print(bow)

    print("\nПерезаряжаем лук на 10 патронов:")
    bow.reload(10)
    print(bow)

    # ----- Сценарий 2 (оценка 4) -----
    print("\n--- Сценарий 2: Полиморфизм и коллекция ---")
    collection = WeaponCollection()
    collection.add(sword)
    collection.add(bow)
    axe = MeleeWeapon("Секира", 50, 80, "common", reach=1.0, material="дерево")
    crossbow = RangedWeapon("Арбалет", 60, 90, "rare", range=200, ammo=5)
    collection.add(axe)
    collection.add(crossbow)

    print("Все предметы в коллекции:")
    for w in collection:
        print(f"  {w}")

    print("\nДемонстрация полиморфизма: вызываем use() для каждого оружия")
    for w in collection:
        print(f"\n--- {w.name} ---")
        try:
            w.use()
        except RuntimeError as e:
            print(f"Ошибка: {e}")

    print("\nПроверка типов через isinstance():")
    for w in collection:
        if isinstance(w, MeleeWeapon):
            print(f"{w.name} - оружие ближнего боя")
        elif isinstance(w, RangedWeapon):
            print(f"{w.name} - оружие дальнего боя")

    # ----- Сценарий 3 (оценка 5) -----
    print("\n--- Сценарий 3: Фильтрация по типу ---")
    melee_only = get_melee(collection)
    ranged_only = get_ranged(collection)

    print("Только оружие ближнего боя:")
    for w in melee_only:
        print(f"  {w.name} (урон {w.damage}, прочность {w.durability})")

    print("\nТолько оружие дальнего боя:")
    for w in ranged_only:
        print(f"  {w.name} (урон {w.damage}, патроны {w.ammo})")

    print("\n--- Интерфейс: вызов use() для всех типов ---")
    for w in collection:
        print(f"\n{w.name}:")
        try:
            w.use()
        except RuntimeError as e:
            print(f"  Не удалось использовать: {e}")

if __name__ == "__main__":
    main()