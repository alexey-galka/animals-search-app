from pydantic import BaseModel


class PasswordRecovery(BaseModel):
    new_password: str
    repeat_password: str


class UserEmail(BaseModel):
    email: str
