from rest_framework import serializers

from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'count' )

    def validate_count(self, value):
        if self.instance and value > self.instance.count:
            raise serializers.ValidationError("Недостаточно доступных книг")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name')


class BuyBookSerializer(serializers.Serializer):
    count = serializers.IntegerField(default=1, min_value=1)


