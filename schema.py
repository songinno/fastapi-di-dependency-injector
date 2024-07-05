from pydantic import BaseModel


class UserRegisterInSchema(BaseModel):
    name: str
    email: str
