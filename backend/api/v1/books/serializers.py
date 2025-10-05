from rest_framework import serializers

from api.v1.books.models import Book, Genre, Author


class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class AuthurSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
