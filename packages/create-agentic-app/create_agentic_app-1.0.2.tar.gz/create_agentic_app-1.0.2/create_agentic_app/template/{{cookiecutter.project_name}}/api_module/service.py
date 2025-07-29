from typing import Dict, List, Optional

from api_module.model import BookCreate


class BookCrud:
    books: Dict = {}

    def get_books(self) -> List[Dict]:
        return list(self.books.values())
    
    def get_book_by_id(self, book_id: int) -> Optional[Dict]:
        return self.books.get(book_id, None)

    def create_book(self, book: BookCreate) -> Dict:
        ids = self.books.keys()
        new_id = max(ids) + 1 if len(ids) != 0 else 1
        new_book = {
            "id": new_id,
            "title": book.title,
            "author": book.author
        }
        self.books[new_id] = new_book
        return new_book
