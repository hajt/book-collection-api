# Book Collection API

*Book Collection is a REST API Web application for browsing book collection with their opinions.*

## Prerequisites

- **Python** >=**3.7.9** with installed dependencies from **requirements.txt**  

## Local development

1. Pull this repository
2. Install the prerequisites
3. Install Python dependencies:   
`pip install -r requirements.txt`
4. Run Python migrations:  
`python manage.py makemigrations` and    
`python manage.py migrate`   
5. Load example ***ksiazki.csv*** and ***opinie.csv*** data:  
`python manage.py import --path <full_path_to_ksiazki.csv>` and  
`python manage.py import --path <full_path_to_opinie.csv>`  
6. Run Django server:  
`python manage.py runserver`

## Available API actions

Retrieve all books:  
`GET /api/books/`  
Retrieve all opinions:  
`GET /api/opinions/`  
Retrieve specific opinion:  
`GET /api/opinions/<opinion_id>/`

## API filtering by query strings  
Retrieve filtered books:  
`GET /api/books/?<query_strings>`  

### Possible filters:
Filter by full title (ignores capitals/lower cases):  
`?title__iexact=<title>`  
Filter by title contains:  
`?title__contains=<title>`  

*Example request:*  
`GET /api/books/?title__contains=osiedle`
