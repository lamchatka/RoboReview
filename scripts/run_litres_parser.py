import os
import django

from parsers.litres_parser.litres_parser import LitresParser

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RoboReview.settings')
django.setup()


if __name__ == "__main__":
    book_url = "https://www.litres.ru/example-book/"
    reviews = LitresParser.get_reviews(book_url, max_reviews=10)
    for review in reviews:
        print(review)
