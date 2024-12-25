from django.db import models
from django.contrib.auth.models import AbstractUser

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
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100)
    published_year = models.IntegerField()
    # добавить descriptionё


# Отзыв
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    source = models.CharField(max_length=100)
    sentiment = models.CharField(max_length=20, choices=[('positive', 'Positive'), ('negative', 'Negative')])
    created_at = models.DateTimeField(auto_now_add=True)


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
