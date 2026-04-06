from weapon import Weapon
from weapon_collection import WeaponCollection

def main():
    # Создаём оружие
    sword = Weapon("Меч", 25, 100, "rare")
    axe = Weapon("Топор", 35, 80, "common")
    bow = Weapon("Лук", 20, 100, "epic")
    dagger = Weapon("Кинжал", 15, 50, "common")

    # ----- Оценка 3 -----
    print("=== Оценка 3 ===")
    armory = WeaponCollection()
    armory.add(sword)
    armory.add(axe)
    armory.add(bow)
    print("После добавления:", [w.name for w in armory.get_all()])

    armory.remove(axe)
    print("После удаления топора:", [w.name for w in armory.get_all()])

    try:
        armory.add("Not a weapon")
    except TypeError as e:
        print("Ошибка типа:", e)

    # ----- Оценка 4 -----
    print("\n=== Оценка 4 ===")
    armory.add(axe)  # возвращаем топор
    armory.add(dagger)

    print("Поиск по имени 'Лук':", [w.name for w in armory.find_by_name("Лук")])
    print("Поиск по урону 35:", [w.name for w in armory.find_by_damage(35)])

    print("Количество предметов:", len(armory))
    print("Итерация по коллекции:")
    for w in armory:
        print(f"  - {w.name} (урон {w.damage})")

    # Проверка дубликатов
    sword_copy = Weapon("Меч", 25, 100, "rare")
    try:
        armory.add(sword_copy)
    except ValueError as e:
        print("Ошибка дубликата:", e)

    # ----- Оценка 5 -----
    print("\n=== Оценка 5 ===")
    print("Первый элемент:", armory[0].name)
    print("Третий элемент:", armory[2].name)

    armory.remove_at(1)
    print("После удаления индекса 1:", [w.name for w in armory])

    armory.sort(key='damage')
    print("Сортировка по урону (возрастание):", [(w.name, w.damage) for w in armory])

    armory.sort(key='name', reverse=True)
    print("Сортировка по имени (обратная):", [w.name for w in armory])

    # Используем оружие, чтобы оно сломалось
    print("\n--- Испытание оружия ---")
    for _ in range(3):
        try:
            sword.use()
            print(f"{sword.name}: прочность {sword.durability}")
        except RuntimeError as e:
            print(e)

    broken_collection = armory.get_broken()
    print("Сломанное оружие:", [w.name for w in broken_collection])

    strong_weapons = armory.get_by_min_damage(25)
    print("Оружие с уроном >= 25:", [w.name for w in strong_weapons])

    rare_weapons = armory.filter(lambda w: w.rarity == "rare")
    print("Редкое оружие:", [w.name for w in rare_weapons])

if __name__ == "__main__":
    main()