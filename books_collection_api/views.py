from rest_framework import generics, viewsets, mixins

from books_collection_api.models import Book, Opinion
from books_collection_api.serializers import BookSerializer, OpinionSerializer


class BookListView(generics.ListAPIView):
    """ List view of books. """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class OpinionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """ List and detail view of opinions. """
    queryset = Opinion.objects.all()
    serializer_class = OpinionSerializer
