from django.test import TestCase
from .models import Book, Author
# Create your tests here.


class TestBook(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="Test", last_name="Author")
        for book in range(10):
            Book.objects.create(title=f"Book {book+1}", author_id=self.author.id, count=10)


    def test_pagination_books_view(self):
        """Тест представления пагинации"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 10)
        self.assertEqual(len(response.json()['results']), 5)


    def test_view_book_list(self):
        """Тест проверки запроса получения книг"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)

    def test_view_book_detail(self):
        """Тест проверки запроса получения одной книги"""

        book = Book.objects.first()
        response = self.client.get(f'/api/books/{book.id}/')
        self.assertEqual(response.status_code, 200)

    
    def test_crerate_book(self):
        """Тест проверки запроса для создания книги"""

        data_book = {
            'title': 'New Book',
            'author': self.author.id,
            'count': 15,
        }
        response = self.client.post(f'/api/books/', data=data_book, content_type='application/json')
    
        self.assertEqual(response.status_code, 201)

    def test_update_book(self):
        """Тест проверки запроса обновление книги"""

        book = Book.objects.first()
        data_book = {
            'title': 'Updated Book',
            'author': self.author.id,
            'count': 10,
        }
        response = self.client.put(f'/api/books/{book.id}/', data=data_book, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_buy_book_view(self):
        """Тест представления покупки книги"""

        book = Book.objects.first()
        data = {'count':15}
        response = self.client.post(f'/api/books/{book.id}/buy/', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_buy_book_method(self):
        """Тест проверки метода покупки книги"""
        book = Book.objects.first()
        book.buy_book(5)
        book.refresh_from_db()
        self.assertEqual(book.count, 5)

    def test_buy_book_gt_method(self):
        """Тест проверки метода покупки книги если количество больше чем есть"""
        book = Book.objects.first()
        book.buy_book(15)
        book.refresh_from_db()
        self.assertEqual(book.count, 10)
        

        
        
class TestAuthor(TestCase):
    def setUp(self):
        self.first_name = 'John'
        self.last_name = 'Doe'

    def test_author_list_view(self):
        """Тест представления списка авторов"""
        response = self.client.get('/api/author/', )
        self.assertEqual(len(response.json()), 0)
        self.assertEqual(response.status_code, 200)

    def test_author_detail_view(self):
        """Тест представления детального автора"""
        author = Author.objects.create(first_name=self.first_name, last_name=self.last_name)
        response = self.client.get(f'/api/author/{author.id}/')
        self.assertEqual(response.status_code, 200)

    def test_author_create_view(self):
        """Тест представления создания автора"""
        data = {'first_name': self.first_name, 'last_name': self.last_name}
        response = self.client.post('/api/author/', data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
    
    def test_update_author_view(self):
        """Тест представления обновления автора"""
        author = Author.objects.create(first_name=self.first_name, last_name=self.last_name)
        data = {'first_name': 'Updated', 'last_name': 'Author'}
        response = self.client.put(f'/api/author/{author.id}/', data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['first_name'], 'Updated')
