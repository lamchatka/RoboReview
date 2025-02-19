from django.core.management.base import BaseCommand
from parsers.litres_parser.litres_parser import LitresParser
from robo_review.models import Book, Review
from datetime import datetime
import locale


class Command(BaseCommand):
    help = "Тестирует сохранение данных из парсера Литрес в БД"

    def handle(self, *args, **kwargs):
        litres_parser = LitresParser()
        book_url = (
            "https://www.litres.ru/book/konstantin-demchuk-8/ot-tryapki-do-titana-duha-nastolnaya-kniga-o-razvitii"
            "-67923051/"
        )
        book_title = "От тряпки до титана духа. Настольная книга о развитии силы воли"
        reviews: list[dict] = litres_parser.get_reviews(book_url, max_reviews=12)

        # book = None
        # try:
        #     book = Book.objects.get(title=book_title)
        #
        # except Book.DoesNotExist:
        #     book = Book.objects.create(
        #         title=book_title,
        #         author="Константин Демчук",
        #         isbn="9785044575707",
        #         genre="Саморазвитие",
        #         published_year=2022
        #     )

        # TODO: Откуда брать данные для создания новой книги, ведь юзер вводит только название. Может парсить их?
        book, created = Book.objects.get_or_create(
            title=book_title,
            author="Константин Демчук",
            isbn="9785044575707",
            genre="Саморазвитие",
            published_year=2022)

        if created:
            print(f"Создана новая книга: {book.author} - {book}")
        else:
            print(f"Книга с таким названием существует: {book}")

        # TODO: правильно преобразовать строку в объект datetime
        # locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")  # Устанавливаем русскую локаль
        # raw_date = "15 января 2024, 18:54"
        # parsed_date = datetime.strptime(raw_date, "%d %B %Y, %H:%M")
        # print(parsed_date)
        # review["review_date"], review["review_time"] = datetime.strptime()

        # TODO: Дублирование отзывов при повторном создании,
        for review in reviews:
            Review.objects.create(
                book=book,
                author_nickname=review["author_nickname"],
                text=review["text"],
                source=review["source"],
            )

        print(f"Успешно сохранено {len(reviews)} отзывов!")

