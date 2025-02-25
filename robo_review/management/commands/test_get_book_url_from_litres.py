from django.core.management import BaseCommand
from parsers.litres_parser.get_book_url_from_litres import get_book_url_from_litres
from robo_review.models import Book


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        books = Book.objects.only("title", "author")
        for book in books:
            print(get_book_url_from_litres(book.title, book.author))
