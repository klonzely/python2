# demo.py
from models import MeleeWeapon, RangedWeapon
from container import TypedCollection, Displayable, Scorable

def main():
    print("=" * 70)
    print("Лабораторная работа №6 — Аннотации типов, Generics, Protocols")
    print("=" * 70)

    # ---------- 1. Создание типизированной коллекции (оценка 3) ----------
    weapons: TypedCollection[MeleeWeapon] = TypedCollection()
    sword = MeleeWeapon("Экскалибур", 20.0, "legendary", level=3, sharpness=1.5)
    dagger = MeleeWeapon("Кинжал", 8.0, "common", level=1)

    weapons.add(sword)
    weapons.add(dagger)
    print("\n[Сценарий 1] Типизированная коллекция MeleeWeapon:")
    for w in weapons.get_all():
        print(f"  {w.display()}")

    # Попытка добавить неподходящий тип (раскомментировать для проверки ошибки типа)
    # weapons.add(RangedWeapon("Лук", 12.0, "rare"))  # IDE подсветит ошибку

    # ---------- 2. find, filter, map (оценка 4) ----------
    print("\n[Сценарий 2] Использование find, filter, map")
    # find: ищем оружие с уровнем >= 2
    found = weapons.find(lambda w: w.level >= 2)
    print(f"find (level>=2): {found.display() if found else 'None'}")

    # filter: все оружия с уроном > 10
    high_damage = weapons.filter(lambda w: w.damage > 10)
    print("filter (damage>10):")
    for w in high_damage:
        print(f"  {w.display()}")

    # map: преобразование в строки имён
    names = weapons.map(lambda w: w.name)
    print(f"map -> list[str] (имена): {names}")

    # map: преобразование в числа (score)
    scores = weapons.map(lambda w: w.score())
    print(f"map -> list[float] (score): {scores}")

    # ---------- 3. Protocol и TypeVar с bound (оценка 5) ----------
    print("\n[Сценарий 3] Работа с протоколами Displayable и Scorable")
    # Создаём коллекцию, работающую только с Displayable-объектами
    displayable_collection: TypedCollection[Displayable] = TypedCollection()

    # Добавляем объекты разных типов, у которых есть метод display()
    # MeleeWeapon и RangedWeapon не наследуются от Displayable, но имеют метод display()
    bow = RangedWeapon("Длинный лук", 12.0, "rare", level=2, ammo=5)
    displayable_collection.add(sword)
    displayable_collection.add(bow)

    print("Displayable-коллекция (вызов display()):")
    for item in displayable_collection.get_all():
        print(f"  {item.display()}")   # здесь item известен как Displayable, есть метод display

    # Создаём коллекцию, работающую с Scorable
    scorable_collection: TypedCollection[Scorable] = TypedCollection()
    scorable_collection.add(sword)
    scorable_collection.add(dagger)
    scorable_collection.add(bow)

    print("\nScorable-коллекция (вызов score()):")
    for item in scorable_collection.get_all():
        print(f"  {item.display()} -> очки: {item.score():.2f}")

    # Сортировка по score с использованием map и sorted
    sorted_scores = sorted(scorable_collection.map(lambda s: s.score()), reverse=True)
    print(f"Отсортированные scores (по убыванию): {sorted_scores}")

    # ---------- 4. Вывод об использовании аннотаций ----------
    print("\n[Итог] Статическая типизация помогает:")
    print("- IDE подсказывает методы (например, .display(), .score())")
    print("- Ошибки несовместимости типов обнаруживаются до выполнения")
    print("- Код становится самодокументированным")

if __name__ == "__main__":
    main()