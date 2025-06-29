from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# ✅ Book model
class Book(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year: Optional[int] = None  # Optional field

# ✅ In-memory list to store books
books: List[Book] = []

# ✅ Home route
@app.get("/")
def home():
    return {"message": "📚 Welcome to the Book Library API"}

# ✅ Get all books
@app.get("/books")
def get_books():
    return books

# ✅ Get book by ID
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}

# ✅ Add a new book
@app.post("/books")
def add_book(book: Book):
    books.append(book)
    return {"message": "Book added successfully", "book": book}

# ✅ Update a book
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = updated_book
            return {"message": "Book updated", "book": updated_book}
    return {"error": "Book not found"}

# ✅ Delete a book
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            deleted = books.pop(index)
            return {"message": "Book deleted", "book": deleted}
    return {"error": "Book not found"}
