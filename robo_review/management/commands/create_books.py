from django.core.management import BaseCommand
from robo_review.models import Book

# TODO: Этот список будет получен в результате парсинга
BOOKS: list[tuple] = [
    ("Война и мир", "Лев Толстой", "978-5-17-118366-6", "Роман", 1869),
    ("Преступление и наказание", "Фёдор Достоевский", "978-5-17-118367-3", "Роман", 1866),
    ("Гордость и предубеждение", "Джейн Остин", "978-5-17-118368-0", "Роман", 1813),
    ("1984", "Джордж Оруэлл", "978-5-17-118369-7", "Антиутопия", 1949),
    ("Убить пересмешника", "Харпер Ли", "978-5-17-118370-3", "Роман", 1960),
    ("Мастер и Маргарита", "Михаил Булгаков", "978-5-17-118371-0", "Мистика", 1967),
    ("Анна Каренина", "Лев Толстой", "978-5-17-118372-7", "Роман", 1877),
    ("451 градус по Фаренгейту", "Рэй Брэдбери", "978-5-17-118373-4", "Фантастика", 1953),
    ("Большие надежды", "Чарльз Диккенс", "978-5-17-118374-1", "Роман", 1861),
    ("О дивный новый мир", "Олдос Хаксли", "978-5-17-118375-8", "Антиутопия", 1932),
    ("Лолита", "Владимир Набоков", "978-5-17-118376-5", "Роман", 1955),
    ("Братья Карамазовы", "Фёдор Достоевский", "978-5-17-118377-2", "Роман", 1880),
    ("Гроздья гнева", "Джон Стейнбек", "978-5-17-118378-9", "Роман", 1939),
    ("Три товарища", "Эрих Мария Ремарк", "978-5-17-118379-6", "Роман", 1936),
    ("Моби Дик", "Герман Мелвилл", "978-5-17-118380-2", "Роман", 1851),
    ("Портрет Дориана Грея", "Оскар Уайльд", "978-5-17-118381-9", "Роман", 1890),
    ("Доктор Живаго", "Борис Пастернак", "978-5-17-118382-6", "Роман", 1957),
    ("Старик и море", "Эрнест Хемингуэй", "978-5-17-118383-3", "Повесть", 1952),
    ("Маленький принц", "Антуан де Сент-Экзюпери", "978-5-17-118384-0", "Сказка", 1943),
    ("Гамлет", "Уильям Шекспир", "978-5-17-118385-7", "Трагедия", 1603),
]


class Command(BaseCommand):
    help = "Создает книги в БД из заранее подготовленного списка"

    def handle(self, *args, **options):
        books_to_create = []
        existing_books = set(Book.objects.values_list("isbn", flat=True))
        for title, author, isbn, genre, published_year in BOOKS:
            if isbn not in existing_books:
                books_to_create.append(Book(
                    title=title,
                    author=author,
                    isbn=isbn,
                    genre=genre,
                    published_year=published_year
                ))
            existing_books.add(isbn)

        if books_to_create:
            Book.objects.bulk_create(books_to_create)
            self.stdout.write(self.style.SUCCESS(f"Успешно добавлено {len(books_to_create)} книг в базу данных"))
        else:
            self.stdout.write(self.style.WARNING("Все книги уже существуют в базе данных"))
