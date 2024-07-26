from typing import List

from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends
from .schemas import Book, CreateBook, Author, CreateAuthor, UpdateAuthor, UpdateBook
from .database import SessionLocal
from .crud import book_list, book_create, book_retrieve, author_list, author_create, author_retrieve, book_delete, \
    book_update, author_update, author_delete


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

books_data = [
    {
        'id': 1,
        'title': 'Python',
        'description': 'Desc 1',
        'author': 'Dmitriy',
        'price': 200,
        'published_year': 2000
    },{
        'id': 2,
        'title': 'Python 2',
        'description': 'Desc 2',
        'author': 'Taras',
        'price': 400,
        'published_year': 2010
    },{
        'id': 3,
        'title': 'Django',
        'description': 'Desc 3',
        'author': 'Andriy',
        'price': 1000,
        'published_year': 2020
    }
]


@app.get('/books/')
async def get_book_list(db: Session = Depends(get_db)) -> List[Book]:
    books = book_list(db)
    return books


@app.get("/books/{book_id}")
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = book_retrieve(db, book_id)
    return book


@app.post("/books/", response_model=Book, status_code=201)
async def create_book(book: CreateBook, db: Session = Depends(get_db)):
    return book_create(db, book)


@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: UpdateBook, db: Session = Depends(get_db)):
    return book_update(db, book_id, book)


@app.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    return book_delete(db, book_id)


@app.get("/authors/")
async def get_authors_list(db: Session = Depends(get_db)) -> List[Author]:
    authors = author_list(db)
    return authors


@app.get("/authors/{author_id}")
async def get_author(author_id: int, db: Session = Depends(get_db)):
    author = author_retrieve(db, author_id)
    return author


@app.post("/authors/", response_model=Author, status_code=201)
async def create_author(author: CreateAuthor, db: Session = Depends(get_db)):
    return author_create(db, author)


@app.put("/authors/{author_id}", response_model=Author)
async def update_author(author_id: int, author: UpdateAuthor, db: Session = Depends(get_db)):
    return author_update(db, author_id, author)


@app.delete("/authors/{author_id}", response_model=Author)
async def delete_author(author_id: int, db: Session = Depends(get_db)):
    return author_delete(db, author_id)
