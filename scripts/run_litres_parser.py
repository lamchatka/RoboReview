import os
import django
from parsers.litres_parser.litres_parser import LitresParser
import locale

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RoboReview.settings')
django.setup()


if __name__ == "__main__":
    book_url = ("https://www.litres.ru/book/konstantin-demchuk-8/ot-tryapki-do-titana-duha-nastolnaya-kniga-o-razvitii"
                "-67923051/")

    reviews = LitresParser.get_reviews(book_url, max_reviews=1)
    for review in reviews:
        print(review)
