from typing import Iterator
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
import ulid

from src.seedx_support_backend.infrastructure.repository import RepositoryInterface, EntityNotFound
from .models import User


class UserRepository(RepositoryInterface[User]):
    def __init__(self, db: Session):
        self.db = db

    def save(self, entity: User) -> User:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def save_all(self, entities: list[User]):
        self.db.add_all(entities)
        self.db.commit()

    def find_all(self) -> Iterator[User]:
        return iter(self.db.query(User).all())

    def find_one(self, id: ulid.ULID) -> User:
        user = self.db.query(User).filter(User.id == str(id)).first()
        if not user:
            raise EntityNotFound(f"User with id {id} not found")
        return user

    def delete_one(self, id: ulid.ULID):
        user = self.find_one(id)
        self.db.delete(user)
        self.db.commit()

    def find_all_by(self, **kwargs) -> Iterator[User]:
        return iter(self.db.query(User).filter_by(**kwargs).all())

    def find_all_by_dict(self, criteria: dict) -> Iterator[User]:
        return iter(self.db.query(User).filter_by(**criteria).all())

    def count_all_by_dict(self, criteria: dict) -> int:
        return self.db.query(User).filter_by(**criteria).count()

    def delete_all(self):
        self.db.query(User).delete()
        self.db.commit()

    def close(self):
        self.db.close()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
