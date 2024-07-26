from pydantic import BaseModel


class BaseBook(BaseModel):
    title: str
    description: str | None = None
    author_id: int
    price: int
    published_year: int


class CreateBook(BaseBook):
    pass


class UpdateBook(BaseBook):
    pass


class Book(BaseBook):
    id: int

    class Config:
        from_attributes = True


class BaseAuthor(BaseModel):
    first_name: str
    last_name: str


class CreateAuthor(BaseAuthor):
    pass


class UpdateAuthor(BaseAuthor):
    pass


class Author(BaseAuthor):
    id: int

    class Config:
        from_attributes = True
