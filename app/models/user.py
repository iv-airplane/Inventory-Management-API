import enum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

# Specification for a database table. Represents the role. Currently, we have two types of roles: user and admin.
# The role determines what actions can be performed on the database.
class Role(str, enum.Enum):
    user = "user"
    admin = "admin"

# Specification for a database table. Represents the user of the server.
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.user, nullable=False)
