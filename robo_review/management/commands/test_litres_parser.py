from django.core.management.base import BaseCommand
from parsers.litres_parser.litres_parser import LitresParser
from robo_review.models import Book, Review
from datetime import datetime
from django.utils import timezone


class Command(BaseCommand):
    help = "Тестирует сохранение данных из парсера Литрес в БД"

    def handle(self, *args, **kwargs):
        """
            1. Создает или получает книгу по названию.
            2. Получает все отзывы из БД, и, если их нет, то сохраняют
        """
        litres_parser = LitresParser()
        book_url = (
            "https://www.litres.ru/book/konstantin-demchuk-8/ot-tryapki-do-titana-duha-nastolnaya-kniga-o-razvitii"
            "-67923051/"
        )
        book_title = "От тряпки до титана духа. Настольная книга о развитии силы воли"
        reviews: list[dict] = litres_parser.get_reviews(book_url, max_reviews=12)

        # TODO: Откуда брать данные для создания новой книги, ведь юзер вводит только название. Может парсить их?
        book, created = Book.objects.get_or_create(
            title=book_title,
            author="Константин Демчук",
            isbn="9785044575707",
            genre="Саморазвитие",
            published_year=2022
        )

        if created:
            print(f"Создана новая книга: {book.author} - {book}")
        else:
            print(f"Книга с таким названием существует: {book}")

        # Создаем множество кортежей (уникальность по 4 полям: book, author_nickname, text, source
        existing_reviews = set(
            Review.objects.filter(book=book).values_list("author_nickname", "text", "source")
        )
        new_reviews = []
        for review in reviews:
            parsed_datetime = datetime.strptime(f"{review['review_date']} {review['review_time']}", "%d.%m.%Y %H:%M")
            aware_date_time = timezone.make_aware(parsed_datetime)
            print(aware_date_time)
            review_tuple = (review["author_nickname"], review["text"], review["source"])
            if review_tuple not in existing_reviews:
                new_reviews.append(
                    Review(
                        book=book,
                        author_nickname=review["author_nickname"],
                        text=review["text"],
                        source=review["source"],
                        review_date=aware_date_time
                    )
                )
            existing_reviews.add(review_tuple)

        # Позволяет сохранить список объектов new_reviews в БД за один запрос
        if new_reviews:
            Review.objects.bulk_create(new_reviews)
            print(f"Успешно сохранено {len(new_reviews)} новых отзывов!")
        else:
            print("Все отзывы уже существуют!")
