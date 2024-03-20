from pydantic import BaseModel


class PasswordReset(BaseModel):
    password: str
    new_password: str
