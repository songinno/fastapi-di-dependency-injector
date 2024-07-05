from typing import List
from sqlalchemy.orm.scoping import ScopedSession
from model import User

class Repository:
    def __init__(self, session_factory: ScopedSession) -> None:
        self.session_factory = session_factory

    def get(self, ref: str) -> User:
        with self.session_factory() as session:
            return session.query(User).filter_by(id=ref).first()

    def add(self, user: User) -> None:
        with self.session_factory() as session:
            session.add(user)
            session.commit()

    def fetch_all(self) -> List[User]:
        with self.session_factory() as session:
            return session.query(User).all();

    def delete_user(self, user_id: str) -> None:
        with self.session_factory() as session:
            found_user = session.query(User).filter_by(id=user_id).first()

            if not found_user:
                raise
            session.delete(found_user)
            session.commit()
