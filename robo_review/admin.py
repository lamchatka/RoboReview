from django.contrib import admin
from .models import User, Book, Review, Recommendation, Report, BookSource, Source

# Register your models here.

admin.site.register(User)
admin.site.register(Book)  # Добавить сортировку по алфавиту, по дате и времени добавления
admin.site.register(Review)
admin.site.register(Recommendation)
admin.site.register(Report)
admin.site.register(BookSource)
admin.site.register(Source)
