# demo.py
from .weapon import Weapon

def main():
    print("=" * 50)
    print("Демонстрация работы класса Weapon")
    print("=" * 50)

    # 1. Создание объектов
    try:
        sword = Weapon("Меч-кладенец", damage=15.0, rarity="legendary", level=3)
        bow = Weapon("Длинный лук", damage=8.5, rarity="rare", level=1)
        dagger = Weapon("Кинжал", damage=5.0, rarity="common", level=2)
        print("\n[1] Созданы объекты:")
        print(sword)
        print(bow)
        print(dagger)
    except (TypeError, ValueError) as e:
        print(f"Ошибка создания: {e}")

    # 2. Вывод через print (используется __str__)
    print("\n[2] Вывод через print (__str__):")
    print(sword)
    print(bow)

    # 3. Сравнение объектов (__eq__)
    sword2 = Weapon("Меч-кладенец", damage=15.0, rarity="legendary", level=3)
    print("\n[3] Сравнение объектов:")
    print(f"sword == sword2? {sword == sword2}")          # True
    print(f"sword == bow? {sword == bow}")                # False

    # 4. Некорректное создание (обработка исключений)
    print("\n[4] Попытка создания с некорректными данными:")
    try:
        bad_weapon = Weapon("", damage=-5, rarity="mythic", level=20)
    except (TypeError, ValueError) as e:
        print(f"   Ошибка: {e}")

    # 5. Изменение свойства через setter (уровень)
    print("\n[5] Изменение уровня через setter:")
    print(f"   До: {bow}")
    bow.level = 5
    print(f"   После: {bow}")
    try:
        bow.level = 15  # превышение MAX_LEVEL
    except ValueError as e:
        print(f"   Ошибка при попытке установить 15: {e}")

    # 6. Доступ к атрибуту класса
    print("\n[6] Доступ к атрибуту класса:")
    print(f"   Через класс Weapon.MAX_LEVEL = {Weapon.MAX_LEVEL}")
    print(f"   Через экземпляр sword.MAX_LEVEL = {sword.MAX_LEVEL}")
    print(f"   Через класс Weapon.VALID_RARITIES = {Weapon.VALID_RARITIES}")

    # 7. Демонстрация бизнес-методов и логических состояний
    print("\n[7] Сценарии работы с состояниями:")

    # Сценарий 1: обычное использование
    print("\n   --- Сценарий 1: обычное использование ---")
    print(f"   {sword}")
    print(f"   Урон при атаке: {sword.attack():.2f}")
    sword.upgrade()
    print(f"   После upgrade: {sword}")
    print(f"   Урон после улучшения: {sword.attack():.2f}")

    # Сценарий 2: поломка и ремонт
    print("\n   --- Сценарий 2: поломка и ремонт ---")
    print(f"   {dagger}")
    dagger.break_weapon()
    print(f"   После поломки: {dagger}")
    print(f"   Попытка атаки сломанным оружием: урон = {dagger.attack()}")
    try:
        dagger.upgrade()
    except ValueError as e:
        print(f"   Попытка улучшить сломанное: {e}")
    dagger.repair()
    print(f"   После ремонта: {dagger}")
    print(f"   Урон после ремонта: {dagger.attack():.2f}")

    # Сценарий 3: граничные значения и валидация
    print("\n   --- Сценарий 3: граничные значения ---")
    try:
        max_weapon = Weapon("Макс", damage=100, rarity="epic", level=Weapon.MAX_LEVEL)
        print(f"   Создано оружие максимального уровня: {max_weapon}")
        max_weapon.upgrade()  # попытка превысить максимум
    except ValueError as e:
        print(f"   Ошибка при upgrade: {e}")

    # Дополнительно: проверка работы __repr__
    print("\n[8] Техническое представление (__repr__):")
    print(repr(sword))

if __name__ == "__main__":
    main()