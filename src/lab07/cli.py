from typing import List
from models import MeleeWeapon, RangedWeapon
from app import WeaponApp
from exceptions import DuplicateItemError, ItemNotFoundError, InvalidInputError
import strategies

class CLI:
    """Консольное меню для управления оружием."""
    def __init__(self, app: WeaponApp) -> None:
        self._app = app

    def _print_menu(self) -> None:
        print("\n" + "="*50)
        print("    УПРАВЛЕНИЕ ОРУЖИЕМ")
        print("="*50)
        print("1. Добавить оружие")
        print("2. Показать всё оружие")
        print("3. Найти оружие по имени")
        print("4. Удалить оружие")
        print("5. Фильтровать оружие")
        print("6. Сортировать оружие")
        print("7. Применить стратегию обработки")
        print("0. Сохранить и выйти")
        print("="*50)

    def _input_number(self, prompt: str, default: int = None) -> int:
        """Безопасный ввод целого числа."""
        while True:
            try:
                val = input(prompt).strip()
                if not val and default is not None:
                    return default
                return int(val)
            except ValueError:
                print("Ошибка: введите целое число.")

    def _input_float(self, prompt: str) -> float:
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Ошибка: введите число (например, 15.5).")

    def _input_str_nonempty(self, prompt: str) -> str:
        while True:
            s = input(prompt).strip()
            if s:
                return s
            print("Ошибка: значение не может быть пустым.")

    def _add_weapon(self) -> None:
        print("\n--- Добавление оружия ---")
        typ = self._input_number("Тип (1 - ближнее, 2 - дальнее): ")
        name = self._input_str_nonempty("Название: ")
        damage = self._input_float("Базовый урон: ")
        rarity = self._input_str_nonempty("Редкость (common/rare/epic/legendary): ")
        level = self._input_number("Уровень (1-10): ", default=1)
        try:
            if typ == 1:
                sharpness = self._input_float("Острота (множитель, по умолч. 1.0): ")
                weapon = MeleeWeapon(name, damage, rarity, level, sharpness if sharpness else 1.0)
            elif typ == 2:
                ammo = self._input_number("Количество патронов (по умолч. 30): ", default=30)
                weapon = RangedWeapon(name, damage, rarity, level, ammo)
            else:
                raise InvalidInputError("Неверный тип оружия")
            self._app.add_weapon(weapon)
            print(f"✓ Оружие '{name}' добавлено.")
        except DuplicateItemError as e:
            print(f" Ошибка: {e}")
        except ValueError as e:
            print(f" Ошибка валидации: {e}")
        except InvalidInputError as e:
            print(f" {e}")

    def _show_all(self) -> None:
        weapons = self._app.get_all()
        if not weapons:
            print("Коллекция пуста.")
            return
        print("\n--- ВСЁ ОРУЖИЕ ---")
        for i, w in enumerate(weapons, 1):
            print(f"{i}. {w.display_info()}")

    def _find_by_name(self) -> None:
        name = self._input_str_nonempty("Введите название: ")
        weapon = self._app.find_by_name(name)
        if weapon:
            print("\nНайдено:")
            print(weapon.display_info())
        else:
            print(f"Оружие '{name}' не найдено.")

    def _remove_weapon(self) -> None:
        name = self._input_str_nonempty("Введите название для удаления: ")
        confirm = input(f"Удалить '{name}'? (y/n): ").lower()
        if confirm != 'y':
            print("Удаление отменено.")
            return
        try:
            removed = self._app.remove_weapon(name)
            print(f"✓ Оружие '{removed.name}' удалено.")
        except ItemNotFoundError as e:
            print(f" {e}")

    def _filter_weapons(self) -> None:
        print("\n--- Фильтрация ---")
        print("1. Только ближнее")
        print("2. Только дальнее")
        print("3. Только исправное")
        print("4. По диапазону базового урона")
        choice = self._input_number("Выберите фильтр: ")
        if choice == 1:
            filtered = self._app.filter_weapons(strategies.is_melee)
        elif choice == 2:
            filtered = self._app.filter_weapons(strategies.is_ranged)
        elif choice == 3:
            filtered = self._app.filter_weapons(strategies.is_not_broken)
        elif choice == 4:
            min_d = self._input_float("Минимальный урон: ")
            max_d = self._input_float("Максимальный урон: ")
            filt = strategies.make_damage_filter(min_d, max_d)
            filtered = self._app.filter_weapons(filt)
        else:
            print("Неверный выбор.")
            return
        if not filtered:
            print("Нет оружия, подходящего под критерии.")
        else:
            print(f"\nНайдено {len(filtered)} единиц:")
            for w in filtered:
                print(f"  {w.display_info()}")

    def _sort_weapons(self) -> None:
        print("\n--- Сортировка ---")
        print("1. По имени (А-Я)")
        print("2. По базовому урону (возрастание)")
        print("3. По уровню (возрастание)")
        print("4. По редкости (common → legendary)")
        print("5. По реальному урону (убывание)")
        choice = self._input_number("Выберите критерий: ")
        reverse = False
        if choice == 1:
            key = strategies.by_name
        elif choice == 2:
            key = strategies.by_damage
        elif choice == 3:
            key = strategies.by_level
        elif choice == 4:
            key = strategies.by_rarity_weight
        elif choice == 5:
            key = strategies.by_total_attack_power
            reverse = True  # сильнейшие первыми
        else:
            print("Неверный выбор.")
            return
        sorted_list = self._app.sort_weapons(key, reverse)
        print("\nОтсортированный список:")
        for w in sorted_list:
            print(f"  {w.display_info()}")

    def _apply_strategy(self) -> None:
        print("\n--- Применить стратегию ко всему оружию ---")
        print("1. Улучшить (повысить уровень)")
        print("2. Поломать всё")
        print("3. Починить всё")
        choice = self._input_number("Выберите стратегию: ")
        if choice == 1:
            strat = strategies.UpgradeStrategy()
        elif choice == 2:
            strat = strategies.BreakAllStrategy()
        elif choice == 3:
            strat = strategies.RepairAllStrategy()
        else:
            print("Неверный выбор.")
            return
        confirm = input("Применить стратегию ко всем объектам? (y/n): ").lower()
        if confirm != 'y':
            print("Отменено.")
            return
        self._app.apply_strategy(strat)
        print("Стратегия применена.")

    def run(self) -> None:
        """Главный цикл CLI."""
        while True:
            self._print_menu()
            choice = self._input_number("Ваш выбор: ")
            if choice == 1:
                self._add_weapon()
            elif choice == 2:
                self._show_all()
            elif choice == 3:
                self._find_by_name()
            elif choice == 4:
                self._remove_weapon()
            elif choice == 5:
                self._filter_weapons()
            elif choice == 6:
                self._sort_weapons()
            elif choice == 7:
                self._apply_strategy()
            elif choice == 0:
                print("Сохраняем данные...")
                self._app.save_data()
                print("До свидания!")
                break
            else:
                print("Неверный пункт меню. Попробуйте снова.")