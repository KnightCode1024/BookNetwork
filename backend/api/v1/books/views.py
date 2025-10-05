from rest_framework import viewsets

from api.v1.books.models import Book, Genre, Author
from api.v1.books import serializers


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializers


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializers


class AuthurViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = serializers.GenreSerializers
