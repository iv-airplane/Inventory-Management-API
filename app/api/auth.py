from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.schemas.user import Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=UserRead)
async def register(body: UserCreate, db: AsyncSession = Depends(get_db)):
    """An endpoint to register user in the database. Checks if the user with this email exists or not"""
    existing = await crud.user.get_user_by_email(db, body.email)
    if existing is not None:
        raise HTTPException(status_code=409, detail="Email already registered")
    return await crud.user.create_user(db, body)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """An endpoint to log the user in after verifying the password"""
    user = await crud.user.get_user_by_email(db, form_data.username)
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return Token(access_token=create_access_token(subject=user.email))
