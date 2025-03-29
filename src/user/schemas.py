from pydantic import BaseModel

class User(BaseModel):
    id: int
    client_id: str
    login: str
    display_name: str
    default_email: str
    is_admin: bool | None = False

class UserEdit(BaseModel):
    login: str
    display_name: str
    default_email: str
    is_admin: bool