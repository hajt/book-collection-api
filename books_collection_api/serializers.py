from rest_framework import serializers

from books_collection_api.models import Book, Opinion


class BookSerializer(serializers.ModelSerializer):
    """ Serializer for Book objects. """
    author = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    opinions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='opinion-detail'
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'category', 'opinions']


class OpinionSerializer(serializers.ModelSerializer):
    """ Serializer for Opinion objects. """
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Opinion
        fields = ['book', 'rate', 'description']
