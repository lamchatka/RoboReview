import requests


def get_book_url_from_litres(book_title: str, author=""):
    """
    Получает URL книги с Литрес, используя API-запрос.
    Что вернет гет запрос на этот эндпоинт
    {
        'status': 200,
        'error': None,
        'payload': {
            'data' : [
                {
                    'type': 'text-book',
                    'instance': {
                        'id': ,
                        'uuid': ,
                        'cover_url': ,
                        'url': ''
                        'title': '',
                        ...
                        ...
                        ...
                    }
                }
            ]
            'extra': {...}
            'facets': [5]
            'fast_facets': []
    }
    """
    base_url: str = "https://api.litres.ru/foundation/api/search"

    # Автора лучше всегда указывать, так запрос будет точнее
    query: str = f"{author} {book_title}"

    # TODO: по ключу types можно выбрать только те типы книг, которые мы хотим получить. Хочу сделать возможность
    #  выбора для юзера
    params = {
        "q": query,
        "is_for_pda": "false",
        "limit": 24,
        "offset": 0,
        "show_unavailable": "false",
        "types": "text_book"
        # "types": [
        #     "text_book", "audiobook", "podcast", "podcast_episode", "webtoon"
        # ]
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/133.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Ошибка запроса ({response.status_code}) для книги: {query}")
        return None

    data = response.json()
    book: dict = data.get("payload", {}).get("data", [])[0]  # Взяли первую найденную книгу
    if not book:
        print(f"Книга '{book_title}' не найдена на Литрес.")
        return None

    instance = book["instance"]
    return f"https://www.litres.ru{instance['url']}"

