import urllib
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from books_collection_api.models import Book, Opinion
from books_collection_api.serializers import BookSerializer, OpinionSerializer
from books_collection_api.tests.test_models import (
    create_sample_author,
    create_sample_category,
    create_sample_book,
    create_sample_opinion
)


def url_with_querystring(path, **kwargs):
    """ Function which joins URL path with query strings. """
    querystrings = urllib.parse.urlencode(kwargs)
    return f"{path}?{querystrings}"


class BookListViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        author = create_sample_author()
        category = create_sample_category()
        create_sample_book(category=category, author=author)
        author = create_sample_author(
            first_name='Adam', second_name='', last_name='Mickiewicz')
        category = create_sample_category(name='Lektury')
        create_sample_book(title='Dziady cz. III',
                           isbn=9321321345432, category=category, author=author)

    def test_retrive_books_all(self):
        """ Test retrieving all books. """
        response = self.client.get(reverse('book-list'))
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrive_books_filtered_by_title(self):
        """ Test retrieving books filtered by full title. """
        title = 'Brzydkie kaczątko'
        url = url_with_querystring(reverse('book-list'), title__iexact=title)
        response = self.client.get(url)
        book = Book.objects.get(title=title)
        serializer = BookSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data[0]), serializer.data)

    def test_retrive_book_by_title_contains(self):
        """ Test retrieving books filtered by title contains. """
        title = 'Dziady'
        url = url_with_querystring(reverse('book-list'), title__contains=title)
        response = self.client.get(url)
        book = Book.objects.get(title__icontains=title)
        serializer = BookSerializer(book)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(response.data[0]), serializer.data)


class OpinionViewSetTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        author = create_sample_author()
        category = create_sample_category()
        book = create_sample_book(category=category, author=author)
        create_sample_opinion(book=book)
        create_sample_opinion(rate=3, description='Test 2', book=book)

    def test_retrive_opinions_all(self):
        """ Test retrieving all opinions. """
        response = self.client.get(reverse('opinion-list'))
        opinions = Opinion.objects.all()
        serializer = OpinionSerializer(opinions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrive_opinion(self):
        """ Test retrieving specific opinion. """
        opinion = Opinion.objects.first()
        url = reverse('opinion-detail', args=[opinion.pk])
        response = self.client.get(url)
        serializer = OpinionSerializer(opinion)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
