import requests
from bs4 import BeautifulSoup


class LitresParser:
    BASE_URL = "https://www.litres.ru"

    @staticmethod
    def get_reviews(book_url, max_reviews=50):
        """
        Парсинг отзывов для заданной книги.
        Отзывы отсортированы по популярности в порядке убывания.

        :param book_url: Ссылка на страницу книги.
        :param max_reviews: Максимальное количество отзывов для парсинга.
        :return: Список словарей с отзывами.
        """
        reviews: list[dict] = []
        page: int = 1

        while len(reviews) < max_reviews:
            # Генерация правильного URL-адреса для страницы отзывов
            reviews_url: str = f"{book_url}otzivi/" if page == 1 else f"{book_url}otzivi/?page={page}"
            print(reviews_url)
            response = requests.get(reviews_url)

            if response.status_code != 200:
                print(f"Ошибка при запросе страницы {reviews_url}")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            all_comments = soup.find('div', class_="AllComments_comments__NJLc7")

            if not all_comments:
                print("Нет отзывов на этой странице.")
                break

            # Обработка того, что может быть добавлены новые комментарии

            # Убираем из выборки комментарии к отзывам
            clear_comments_div = []
            print(len(all_comments))  # 12
            # TODO: мне не нравится, что тут 22 элемента
            print(len(all_comments.find_all("div", attrs={"role": "group"})))  # 22

            for comment_div in all_comments.find_all("div", attrs={"role": "group"}):
                # Проверяем, что у элемента есть ТОЛЬКО нужный класс, чтобы не включать в выборку комментарии к отзывам
                classes = comment_div.get("class", [])
                if classes == ["Comment_comment___A7LB"]:
                    clear_comments_div.append(comment_div)

            print(len(clear_comments_div))  # 10

            for div in clear_comments_div:
                review = LitresParser.parse_review_element(div)
                if review:
                    reviews.append(review)
                    if len(reviews) >= max_reviews:
                        break
            page += 1

        # print(len(reviews))
        return reviews

    @staticmethod
    def parse_review_element(element):
        """
        Парсинг данных отдельного отзыва.

        :param element: HTML-элемент отзыва.
        :return: Словарь с данными отзыва.
        """
        try:
            author_nickname: str = (element
                                    .find("div", class_="Comment_commentTopContent__7rwUh")
                                    .find("div", class_="Avatar_wrapper__sSv4k")
                                    .find("div", class_="Avatar_content__r8ncZ")
                                    .find("div", class_="Avatar_topContent__yt1EN").get_text())

            text: str = element.find("div", class_="Truncate_truncated__jKdVt").get_text()
            review_date, review_time = (element
                                        .find("div", class_="Comment_commentTopContent__7rwUh")
                                        .find("div", class_="Avatar_wrapper__sSv4k")
                                        .find("div", class_="Avatar_content__r8ncZ")
                                        .find("div", class_="Avatar_bottomContent__yyo1q")
                                        .find("time").get("title")).split(",")

        except Exception as e:
            # TODO: Подумать, что делать при ошибках парсинга отзыва; почему может не спарситься один отзыв?
            print(f"Ошибка при парсинге отзыва: {e}")
            return None
        else:
            return {
                "author_nickname": author_nickname,
                "review_date": review_date,
                "review_time": review_time.strip(),
                "text": text,
                "source": "Литрес"
            }
