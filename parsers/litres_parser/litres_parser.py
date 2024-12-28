import requests
from bs4 import BeautifulSoup


class LitresParser:
    BASE_URL = "https://www.litres.ru"

    @staticmethod
    def get_reviews(book_url, max_reviews=50):
        """
        Парсинг отзывов для заданной книги.

        :param book_url: Ссылка на страницу книги.
        :param max_reviews: Максимальное количество отзывов для парсинга.
        :return: Список словарей с отзывами.
        """
        reviews = []
        page = 1

        while len(reviews) < max_reviews:
            # Генерация URL для страницы отзывов
            reviews_url = f"{book_url}page-{page}/#reviews"
            response = requests.get(reviews_url)

            if response.status_code != 200:
                print(f"Ошибка при запросе страницы {reviews_url}")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            review_elements = soup.select("div.review")  # Убедитесь, что этот селектор совпадает с реальным на сайте

            if not review_elements:
                print("Нет отзывов на этой странице.")
                break

            for element in review_elements:
                review = LitresParser.parse_review_element(element)
                if review:
                    reviews.append(review)
                    if len(reviews) >= max_reviews:
                        break

            page += 1

        return reviews

    @staticmethod
    def parse_review_element(element):
        """
        Парсинг отдельного отзыва.

        :param element: HTML-элемент отзыва.
        :return: Словарь с данными отзыва.
        """
        try:
            user_name = element.select_one(".review-author").get_text(strip=True)
            rating = element.select_one(".rating").get("data-rating")  # Пример, уточните на реальном сайте
            text = element.select_one(".review-text").get_text(strip=True)

            return {
                "user_name": user_name,
                "rating": int(rating) if rating else None,
                "text": text,
            }
        except Exception as e:
            print(f"Ошибка при парсинге отзыва: {e}")
            return None
