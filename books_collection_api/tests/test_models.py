from typing import Optional
from django.test import TestCase
from django import db

from books_collection_api.models import Author, Category, Book, Opinion


def create_sample_author(
        first_name: str = 'Hans',
        second_name: str = 'Christian',
        last_name: str = 'Andersen') -> Author:
    """ Creating sample Author object. """
    defaults = {
        'first_name': first_name,
        'second_name': second_name,
        'last_name': last_name
    }
    return Author.objects.create(**defaults)


def create_sample_category(
        name: str = 'Bajka') -> Category:
    """ Creating sample Category object. """
    defaults = {
        'name': name
    }
    return Category.objects.create(**defaults)


def create_sample_book(title: str = 'Brzydkie kaczątko',
                       isbn: int = 9788372783301,
                       category: Optional[Category] = None,
                       author: Optional[Author] = None) -> Book:
    """ Creating sample Book object. """
    defaults = {
        'title': title,
        'isbn': isbn,
        'category': category,
        'author': author
    }
    return Book.objects.create(**defaults)


def create_sample_opinion(rate: int = 5,
                          description: str = "Test 1",
                          book: Optional[Book] = None) -> Opinion:
    """ Creating sample Opinion object. """
    defaults = {
        'rate': rate,
        'description': description,
        'book': book
    }
    return Opinion.objects.create(**defaults)


class AuthorTests(TestCase):

    def test_author_str_with_second_name(self):
        """ Test Author with second name string representation. """
        author = create_sample_author()
        self.assertEqual(str(author), "Hans Christian Andersen")

    def test_author_str_without_second_name(self):
        """ Test Author without second name string representation. """
        author = create_sample_author(
            first_name='Adam', second_name='', last_name='Mickiewicz')
        self.assertEqual(str(author), "Adam Mickiewicz")

    def test_get_or_create_from_str(self):
        """ Test get_or_create_from_string Manager's method. """
        author = 'Adam Mickiewicz'
        author_obj = Author.objects.get_or_create_from_str(author)
        exists = Author.objects.filter(last_name='Mickiewicz').exists()
        self.assertTrue(exists)
        self.assertEqual(author_obj.first_name, 'Adam')
        self.assertEqual(author_obj.second_name, '')
        self.assertEqual(author_obj.last_name, 'Mickiewicz')

    def test_unique_author(self):
        """ Test class unique_constrains. """
        create_sample_author()
        with self.assertRaises(db.utils.IntegrityError) as cm:
            create_sample_author()
        self.assertEqual(str(cm.exception),
                         "UNIQUE constraint failed: books_collection_api_author.first_name, books_collection_api_author.last_name")


class CategoryTests(TestCase):

    def test_category_str(self):
        """ Test Category string representation. """
        category = create_sample_category()
        self.assertEqual(str(category), "Bajka")

    def test_unique_category(self):
        """ Test class unique_constrains. """
        create_sample_category()
        with self.assertRaises(db.utils.IntegrityError) as cm:
            create_sample_category()
        self.assertEqual(str(cm.exception),
                         "UNIQUE constraint failed: books_collection_api_category.name")


class BookTests(TestCase):

    def setUp(self):
        self.author = create_sample_author()
        self.category = create_sample_category()

    def test_book_str(self):
        """ Test Book string representation. """
        book = create_sample_book(
            category=self.category, author=self.author)
        self.assertEqual(str(book),
                         "Brzydkie kaczątko, ISBN: 9788372783301")

    def test_unique_oook(self):
        """ Test class unique_constrains. """
        create_sample_book(category=self.category, author=self.author)
        with self.assertRaises(db.utils.IntegrityError) as cm:
            create_sample_book(category=self.category, author=self.author)
        self.assertEqual(str(cm.exception),
                         "UNIQUE constraint failed: books_collection_api_book.isbn")


class OpinionTests(TestCase):

    def setUp(self):
        self.author = create_sample_author()
        self.category = create_sample_category()
        self.book = create_sample_book(
            category=self.category, author=self.author)

    def test_opinion_str(self):
        """ Test Opinion string representation. """
        opinion = create_sample_opinion(book=self.book)
        self.assertEqual(str(opinion), "5, 'Test 1'")

    def test_couple_opinions(self):
        """ Test Opinion books set. """
        create_sample_opinion(book=self.book)
        create_sample_opinion(rate=4, description='Test 2', book=self.book)
        create_sample_opinion(rate=1, description='Test 3', book=self.book)
        count = self.book.opinions.count()
        self.assertEqual(count, 3)
