from rest_framework import serializers

from .models import Book, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'first_name', 'last_name')

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'count', 'author', )

    def validate_count(self, value):
        if self.instance and value > self.instance.count:
            raise serializers.ValidationError("Недостаточно доступных книг")
        return value


class BuyBookSerializer(serializers.Serializer):
    count = serializers.IntegerField(default=1, min_value=1)


