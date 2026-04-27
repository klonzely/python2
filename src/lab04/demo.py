from models import MeleeWeapon, RangedWeapon
from collection import WeaponInventory
from interfaces import Attackable, Displayable

def print_attack_damage(attacker: Attackable) -> None:
    """Универсальная функция, работающая через интерфейс Attackable."""
    print(f"Урон атаки: {attacker.attack():.2f}")

def main():
    print("=" * 60)
    print("Лабораторная работа №4 — Интерфейсы и абстрактные классы")
    print("=" * 60)

    # 1. Создание объектов разных типов
    sword = MeleeWeapon("Экскалибур", 20.0, "legendary", level=3, sharpness=1.5)
    bow = RangedWeapon("Длинный лук", 12.0, "rare", level=2, ammo=5)
    dagger = MeleeWeapon("Кинжал", 8.0, "common", level=1)

    print("\n[1] Созданы объекты:")
    print(sword.display_info())
    print(bow.display_info())
    print(dagger.display_info())

    # 2. Полиморфизм через интерфейс Attackable
    print("\n[2] Вызов универсальной функции print_attack_damage (интерфейс Attackable):")
    for weapon in (sword, bow, dagger):
        print(f"{weapon.name}: ", end="")
        print_attack_damage(weapon)

    # 3. Работа с коллекцией
    print("\n[3] Создаём коллекцию WeaponInventory и добавляем оружие:")
    inventory = WeaponInventory()
    inventory.add(sword)
    inventory.add(bow)
    inventory.add(dagger)
    inventory.print_all_displayable()

    # 4. Фильтрация по интерфейсу с помощью isinstance
    print("\n[4] Фильтрация объектов, реализующих Displayable:")
    displayable_items = inventory.filter_by_interface(Displayable)
    print(f"Найдено {len(displayable_items)} Displayable объектов")
    for item in displayable_items:
        print(" -", item.display_info())

    # 5. Сортировка по урону через интерфейс Attackable
    print("\n[5] Сортировка оружия по урону (от большего к меньшему):")
    sorted_weapons = inventory.sort_by_attack()
    for w in sorted_weapons:
        print(f"{w.name}: {w.attack():.2f} урона")

    # 6. Демонстрация ремонта и поломки (методы из Weapon)
    print("\n[6] Демонстрация изменения состояния:")
    bow.break_weapon()
    print(f"После поломки: {bow.display_info()}")
    bow.repair()
    print(f"После ремонта: {bow.display_info()}")

    # 7. Проверка множественной реализации интерфейсов
    print("\n[7] Проверка, что объекты реализуют несколько интерфейсов:")
    print(f"sword реализует Attackable? {isinstance(sword, Attackable)}")
    print(f"sword реализует Displayable? {isinstance(sword, Displayable)}")
    print(f"bow реализует Attackable? {isinstance(bow, Attackable)}")
    print(f"bow реализует Displayable? {isinstance(bow, Displayable)}")

    # 8. Ошибки и обработка (из прошлых ЛР)
    print("\n[8] Попытка некорректного улучшения (обработка исключений):")
    try:
        bad_weapon = MeleeWeapon("", -10, "mythic", level=20)
    except (TypeError, ValueError) as e:
        print(f"Ошибка создания: {e}")

if __name__ == "__main__":
    main()