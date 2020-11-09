from django_filters import rest_framework as filters

from books_collection_api.models import Book


class BookFilter(filters.FilterSet):
    """ Book object filter class. """

    class Meta:
        model = Book
        fields = {
            'title': ['iexact', 'contains'],
        }
