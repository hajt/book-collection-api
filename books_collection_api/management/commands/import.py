import os
import csv

from django.core.management.base import BaseCommand, CommandError
from books_collection_api.models import Author, Category, Book, Opinion


BOOKS_FILE = 'ksiazki.csv'
OPINIONS_FILE = 'opinie.csv'


class Command(BaseCommand):
    help = 'Load a data from csv file into the database'

    def add_arguments(self, parser) -> None:
        """ Defining available arguments. """
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options) -> None:
        """ Handling command method. """
        path = options['path']
        if path:
            filename = os.path.split(path)[-1]
            if filename == BOOKS_FILE:
                self._import_books(filename)
            elif filename == OPINIONS_FILE:
                self._import_opinions(filename)

    def _import_books(self, filename: str) -> None:
        """ Function which parses csv file with books 
        and inserts them into the database. """
        with open(filename, 'r') as file:
            total = 0
            reader = csv.reader(file, delimiter=';')
            next(reader)
            for row in reader:
                isbn = row[0]
                title = row[1]
                author = row[2]
                category = row[3]
                author_obj = Author.objects.get_or_create_from_str(
                    author)
                category_obj, created = Category.objects.get_or_create(
                    name=category)
                book_obj, created = Book.objects.get_or_create(
                    title=title, isbn=isbn, author=author_obj, category=category_obj)
                if created:
                    total += 1
            if total:
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully imported {total} books!'))
            else:
                self.stdout.write(self.style.NOTICE('No new books to import.'))

    def _import_opinions(self, filename: str) -> None:
        """ Function which parses csv file with opinions 
        and inserts them into the database. """
        with open(filename, 'r') as file:
            total = 0
            reader = csv.reader(file, delimiter=';')
            next(reader)
            for row in reader:
                isbn = row[0]
                rate = row[1]
                description = row[2]
                try:
                    book_obj = Book.objects.get(isbn=isbn)
                except Book.DoesNotExist:
                    raise CommandError(f'Book with ISBN={isbn} does not exist')
                opinion_obj, created = Opinion.objects.get_or_create(
                    rate=rate, description=description, book=book_obj)
                if created:
                    total += 1
            if total:
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully imported {total} opinions!'))
            else:
                self.stdout.write(self.style.NOTICE(
                    'No new opinions to import.'))
