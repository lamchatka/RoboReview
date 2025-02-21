from django.contrib import admin
from .models import User, Book, Review, Recommendation, Report, BookSource

# Register your models here.

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Recommendation)
admin.site.register(Report)
admin.site.register(BookSource)
