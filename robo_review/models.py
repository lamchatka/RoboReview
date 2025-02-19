from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Уникальное имя для обратной связи
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Уникальное имя для обратной связи
        blank=True
    )


# Книга
class Book(models.Model):
    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100)
    published_year = models.IntegerField()

    # TODO: добавить description и метод str

    def __str__(self):
        return self.title


# Отзыв
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    author_nickname = models.CharField(max_length=70, blank=True, null=True)
    text = models.TextField()
    source = models.CharField(max_length=100)
    sentiment = models.CharField(max_length=20, choices=[('positive', 'Positive'), ('negative', 'Negative')],
                                 blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # отслеживает, дату и время, когда отзыв попал в БД
    review_date = models.DateTimeField(null=True, blank=True)
    # TODO: подумать над моделью отзывов: нужно ли хранить ник автора отзыва
    # TODO: Как оценивать sentiment? По каким метрикам? По rating (кол-во звезд)?


# Рекомендация
class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    books = models.ManyToManyField(Book)
    created_at = models.DateTimeField(auto_now_add=True)


# Отчет
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to='reports/')

# TODO: Добавить модель для хранения агрегированных данных (общая оценка всех отзывов для одной книги) для книг
