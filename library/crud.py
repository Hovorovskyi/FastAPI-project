from sqlalchemy.orm import Session
from typing import Optional

from .models import Book, Author, User, Payment
from .schemas import (
    CreateBook, CreateAuthor, UpdateBook, UpdateAuthor, UserCreate, SubscriptionCreate, Subscription,
    UserUpdate, PaymentCreate
)


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit=10):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def user_create(db: Session, user: UserCreate):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def user_update(db: Session, user_id: int, update_user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    for key, value in update_user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def user_delete(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user


def subscription_create(db: Session, subscription: SubscriptionCreate, user_id: int):
    db_subscription = Subscription(**subscription.model_dump(), user_id=user_id)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def book_list(db: Session):
    return db.query(Book).all()


def book_create(db: Session, book: CreateBook):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def book_retrieve(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def book_update(db: Session, book_id: int, book: UpdateBook):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        for key, value in book.model_dump().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def book_delete(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


def author_list(db: Session):
    return db.query(Author).all()


def author_create(db: Session, author: CreateAuthor):
    db_author = Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def author_retrieve(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def author_update(db: Session, author_id: int, author: UpdateAuthor):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author:
        for key, value in author.model_dump().items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
    return db_author


def author_delete(db: Session, author_id: int):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author


def payment_create(db: Session, payment: PaymentCreate, user_id: int, subscription_id: Optional[int] = None):
    db_payment = Payment(**payment.model_dump(), user_id=user_id, subscription_id=subscription_id)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payments_by_user(db: Session, user_id: int):
    return db.query(Payment).filter(Payment.user_id == user_id).first()
