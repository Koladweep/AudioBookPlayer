import unittest
from unittest.mock import patch, MagicMock
from .librivox_independent import LibriVox, Book, BookItem, BookItems

class TestLibriVox(unittest.TestCase):

    @patch('librivox.ia.get_item')
    def test_get_book(self, mock_get_item):
        # Mock the response from ia.get_item
        mock_item = MagicMock()
        mock_item.get_files.return_value = [
            MagicMock(metadata={
                'name': 'file1.mp3',
                'track': '1',
                'title': 'Chapter 1',
                'length': '00:10:00',
                'creator': 'Author Name'
            })
        ]
        mock_item.metadata = {
            'title': 'Book Title',
            'runtime': '01:00:00',
            'preview': 'preview.jpg',
            'description': 'Book Description'
        }
        mock_get_item.return_value = mock_item

        librivox = LibriVox()
        book = librivox.get_book('https://archive.org/details/book_identifier')

        self.assertEqual(book.author, 'Author Name')
        self.assertEqual(book.name, 'Book Title')
        self.assertEqual(book.duration, 3600)
        self.assertEqual(book.url, 'https://archive.org/details/book_identifier')
        self.assertEqual(book.preview, 'https://archive.org/download/book_identifier/preview.jpg')
        self.assertEqual(book.driver, 'LibriVox')
        self.assertEqual(book.description, 'Book Description')
        self.assertEqual(len(book.items), 1)
        self.assertEqual(book.items[0].file_url, 'https://archive.org/download/book_identifier/file1.mp3')
        self.assertEqual(book.items[0].file_index, 1)
        self.assertEqual(book.items[0].title, 'Chapter 1')
        self.assertEqual(book.items[0].start_time, 0)
        self.assertEqual(book.items[0].end_time, '00:10:00')

    @patch('librivox.ia.search_items')
    @patch('librivox.LibriVox.fetch_books')
    def test_search_books(self, mock_fetch_books, mock_search_items):
        # Mock the response from ia.search_items
        mock_search_items.return_value = [
            {'identifier': 'book1'},
            {'identifier': 'book2'}
        ]

        # Mock the response from fetch_books
        mock_fetch_books.return_value = [
            {
                'author': 'Author 1',
                'title': 'Title 1',
                'duration': 3600,
                'url': 'https://archive.org/details/book1',
                'preview': 'https://archive.org/download/book1/preview.jpg',
                'driver': 'LibriVox'
            },
            {
                'author': 'Author 2',
                'title': 'Title 2',
                'duration': 7200,
                'url': 'https://archive.org/details/book2',
                'preview': 'https://archive.org/download/book2/preview.jpg',
                'driver': 'LibriVox'
            }
        ]

        librivox = LibriVox()
        books = librivox.search_books('test query')

        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].author, 'Author 1')
        self.assertEqual(books[0].name, 'Title 1')
        self.assertEqual(books[0].duration, 3600)
        self.assertEqual(books[0].url, 'https://archive.org/details/book1')
        self.assertEqual(books[0].preview, 'https://archive.org/download/book1/preview.jpg')
        self.assertEqual(books[0].driver, 'LibriVox')

        self.assertEqual(books[1].author, 'Author 2')
        self.assertEqual(books[1].name, 'Title 2')
        self.assertEqual(books[1].duration, 7200)
        self.assertEqual(books[1].url, 'https://archive.org/details/book2')
        self.assertEqual(books[1].preview, 'https://archive.org/download/book2/preview.jpg')
        self.assertEqual(books[1].driver, 'LibriVox')

if __name__ == '__main__':
    unittest.main()