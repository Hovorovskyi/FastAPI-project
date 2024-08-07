import os
import httpx

from typing import List
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from .auth import (
    create_access_token, get_current_user, Token, TokenData, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash,
    verify_password
)
from .schemas import (
    Book, CreateBook, Author, CreateAuthor, UpdateAuthor, UpdateBook, User, UserCreate, Subscription,
    SubscriptionCreate, UserUpdate, Payment, PaymentCreate
)
from .database import SessionLocal
from .crud import (
    book_list, book_create, book_retrieve, author_list, author_create, author_retrieve, book_delete,
    book_update, author_update, author_delete, user_create, get_users, get_user_by_email,
    subscription_create, get_subscription_by_user, subscription_update, subscription_delete,
    user_update, user_delete, payment_create
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


load_dotenv()

app = FastAPI()
router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@router.post("/chat")
async def chet_with_gpt(prompt: str):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="OpenAI API key not found.")

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 50,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=data
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    result = response.json()
    return {"response": result["choices"][0]["message"]["content"]}

app.include_router(router)


@app.post("/register/", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    hashed_password = get_password_hash(user.password)
    db_user = User(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        hashed_password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get("/users/me")
async def read_users_me(current_user: TokenData = Depends(get_current_user)):
    return current_user


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


@app.post("/users/{user_id}/subscriptions/", response_model=Subscription)
async def create_subscription_for_user(user_id: int, subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    return subscription_create(db=db, subscription=subscription, user_id=user_id)


@app.get("/users/{user_id}/subscriptions/", response_model=Subscription)
async def get_subscriptions(user_id: int, db: Session = Depends(get_db)):
    subscriptions = get_subscription_by_user(db=db, user_id=user_id)
    if not subscriptions:
        raise HTTPException(status_code=404, detail="No subscriptions found")
    return subscriptions


@app.put("/subscriptions/{subscription_id}/", response_model=Subscription)
async def update_subscription(subscription_id: int,subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    updated_subscription = subscription_update(db=db, subscription_id=subscription_id, subscription_data=subscription)
    if not updated_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return updated_subscription


@app.delete("/subscriptions/{subscription_id}/", response_model=Subscription)
async def delete_subscription(subscription_id: int, db: Session = Depends(get_db)):
    deleted_subscription = subscription_delete(db=db, subscription_id=subscription_id)
    if not deleted_subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return deleted_subscription

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
