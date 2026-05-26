"""Собственные исключения для предметной области."""

class ItemNotFoundError(Exception):
    """Объект не найден в коллекции."""
    pass

class DuplicateItemError(Exception):
    """Объект с таким именем уже существует."""
    pass

class InvalidInputError(Exception):
    """Некорректный ввод пользователя."""
    pass