from model import User
from repository import Repository


class Service:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def get_by_id(self, id: str):
        return self.repository.get(ref=id)

    def add_new_user(self, name: str, email: str) -> None:
        self.repository.add(User(name=name, email=email))

    def get_all(self):
        return self.repository.fetch_all()

    def delete_user(self, user_id) -> None:
        self.repository.delete_user(user_id=user_id)
