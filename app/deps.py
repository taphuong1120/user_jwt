from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt,JWTError
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserResponse
from app.config import settings
from app.utils import verify_password
from app.database import get_db

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)

async def get_user(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()


async def authenticate_user(username: str, password: str, db: Session):
    user = await get_user(username=username, db=db)

    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(reuseable_oauth)) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = await get_user(db=db,username=username)
        if user is None:
            raise credentials_exception

        return user
    except JWTError:
        raise credentials_exception
