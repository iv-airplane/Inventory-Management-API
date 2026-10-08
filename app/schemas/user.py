from pydantic import BaseModel, ConfigDict

from app.models.user import Role


# Request body for POST /auth/register. Plaintext password in, never stored
# or returned as-is -- it gets hashed before reaching the User model.
class UserCreate(BaseModel):
    email: str
    password: str


# Response body for user-related endpoints. Deliberately has no password
# field, so a User ORM object can never leak its hashed_password through
# this schema even if passed in directly.
class UserRead(BaseModel):
    # Lets Pydantic read fields off a SQLAlchemy User object's attributes,
    # not just from a dict.
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: Role


# Response body for POST /auth/login. access_token is the signed JWT
# (see create_access_token in app/core/security.py); token_type "bearer"
# tells the client how to send it back: an `Authorization: Bearer <token>`
# header on future requests.
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
