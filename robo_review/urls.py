from django.urls import path

from . import views
from .views import BookListView, ReviewListView

urlpatterns = [
    path('', views.index),
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/reviews/', ReviewListView.as_view(), name='review-list'),
]
