from rest_framework import generics, viewsets, mixins

from books_collection_api.models import Book, Opinion
from books_collection_api.serializers import BookSerializer, OpinionSerializer
from books_collection_api.filters import BookFilter


class BookListView(generics.ListAPIView):
    """ List view of books. """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter


class OpinionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """ List and detail view of opinions. """
    queryset = Opinion.objects.all()
    serializer_class = OpinionSerializer
