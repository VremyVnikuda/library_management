# library_manager.py

import json
from typing import List


class Book:
    """
    Класс, представляющий книгу в библиотеке.
    """
    def __init__(self, book_id: int,
                 title: str,
                 author: str,
                 year: int,
                 status: str = "в наличии"):
        """
        Инициализация экземпляра книги.

        :param book_id: Уникальный идентификатор книги.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :param status: Статус книги ("в наличии" или "выдана").
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        """
        Преобразует объект книги в словарь.

        :return: Словарь с атрибутами книги.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict) -> 'Book':
        """
        Создает объект книги из словаря.

        :param data: Словарь с данными книги.
        :return: Экземпляр класса Book.
        """
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
        )


class LibraryManager:
    """
    Класс, управляющий библиотекой.
    """
    def __init__(self, filename: str):
        """
        Инициализация менеджера библиотеки.

        :param filename: Имя файла для хранения данных библиотеки.
        """
        self.filename = filename
        self.books: List[Book] = self._load_from_file()

    def _load_from_file(self) -> List[Book]:
        """
        Загрузка данных библиотеки из файла.

        :return: Список книг.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return [Book.from_dict(book) for book in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_to_file(self) -> None:
        """
        Сохранение данных библиотеки в файл.
        """
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> Book:
        """
        Добавление книги в библиотеку.

        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :return: Добавленная книга.
        """
        book_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        return new_book

    def remove_book(self, book_id: int) -> bool:
        """
        Удаление книги из библиотеки.

        :param book_id: Уникальный идентификатор книги.
        :return: Успешность операции.
        """
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            self.books.remove(book)
            return True
        return False

    def search_books(self, query: str, key: str) -> List[Book]:
        """
        Поиск книг по ключу.

        :param query: Значение для поиска.
        :param key: Поле для поиска ("title", "author", "year").
        :return: Список найденных книг.
        """
        if key not in {"title", "author", "year"}:
            return []
        return [book for book in self.books if query.lower() in str(getattr(book, key, "")).lower()]

    def update_status(self, book_id: int, new_status: str) -> bool:
        """
        Изменение статуса книги.

        :param book_id: Уникальный идентификатор книги.
        :param new_status: Новый статус ("в наличии" или "выдана").
        :return: Успешность операции.
        """
        if new_status not in {"в наличии", "выдана"}:
            return False
        book = next((book for book in self.books if book.id == book_id), None)
        if book:
            book.status = new_status
            return True
        return False

    def display_books(self) -> None:
        """
        Вывод всех книг в библиотеке.
        """
        if not self.books:
            print("Библиотека пуста.")
        else:
            print("Список книг:")
            for book in self.books:
                print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, "
                      f"Год: {book.year}, Статус: {book.status}")


def main():
    """
    Главная функция приложения.
    """
    library = LibraryManager("books.json")

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            try:
                year = int(input("Введите год издания книги: "))
                book = library.add_book(title, author, year)
                print(f"Книга добавлена: {book.to_dict()}")
            except ValueError:
                print("Ошибка: Год издания должен быть числом.")
        elif choice == "2":
            try:
                book_id = int(input("Введите ID книги, которую хотите удалить: "))
                if library.remove_book(book_id):
                    print("Книга успешно удалена.")
                else:
                    print("Ошибка: Книга с указанным ID не найдена.")
            except ValueError:
                print("Ошибка: ID должен быть числом.")
        elif choice == "3":
            key = input("По какому полю искать (title/author/year): ")
            query = input("Введите значение для поиска: ")
            results = library.search_books(query, key)
            if results:
                library.display_books()
            else:
                print("Книги не найдены.")
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            try:
                book_id = int(input("Введите ID книги: "))
                new_status = input("Введите новый статус (в наличии/выдана): ")
                if library.update_status(book_id, new_status):
                    print("Статус книги успешно обновлен.")
                else:
                    print("Ошибка: Книга с указанным ID не найдена.")
            except ValueError:
                print("Ошибка: ID должен быть числом.")
        elif choice == "6":
            library.save_to_file()
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Ошибка: Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
