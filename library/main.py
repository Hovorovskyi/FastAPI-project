from typing import List

from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException
from .schemas import (
    Book, CreateBook, Author, CreateAuthor, UpdateAuthor, UpdateBook, User, UserCreate, Subscription,
    SubscriptionCreate, UserUpdate, Payment, PaymentCreate
)
from .database import SessionLocal
from .crud import (
    book_list, book_create, book_retrieve, author_list, author_create, author_retrieve, book_delete,
    book_update, author_update, author_delete, user_create, get_users, get_user_by_email,
    subscription_create, user_update, user_delete, payment_create
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=404, detail='Email already registered')
    return user_create(db=db, user=user)


@app.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db=db, skip=skip, limit=limit)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_update(db=db, user_id=user_id, update_user=user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_delete(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/subscriptions", response_model=Subscription)
async def create_subscription_for_user(user_id: int, subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    return subscription_create(db=db, subscription=subscription, user_id=user_id)


@app.get("/books/")
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


@app.post("/users/{user_id}/payments/", response_model=Payment)
async def create_payment_for_user(user_id: int, payment: PaymentCreate, db: Session = Depends(get_db)):
    return payment_create(db=db, payment=payment, user_id=user_id)
