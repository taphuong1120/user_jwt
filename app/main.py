from fastapi import FastAPI, status, HTTPException, Depends, Body
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from app.schemas import UserResponse,CreateUserSchema,TokenSchema,UpdateUserSchema
from app.models import User,Base
from app.utils import (
    get_hashed_password,
    create_access_token)
from app.database import get_db
from app.deps import (
    authenticate_user,
    get_current_user,
    )
from app.config import settings
from pydantic import EmailStr

# Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/', response_class=RedirectResponse, include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@app.post('/signup', status_code=status.HTTP_201_CREATED,summary="Create user", response_model=UserResponse)
async def create_user(payload: CreateUserSchema, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(
        User.username == str(payload.username.lower())).first() 
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Account already exist')

    if payload.password != payload.passwordConfirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')
    
    payload.password = get_hashed_password(payload.password)
    del payload.passwordConfirm
    payload.role = 0
    payload.disabled = False
    payload.username = str(payload.username.lower())
    payload.email = EmailStr(payload.email.lower())
    new_user = User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/login', summary="Create access token for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/me/profile', summary='Get details of currently logged in user', response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user



@app.patch('/me/profile', summary='Update of currently logged in user',status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_data: UpdateUserSchema = Body(...), current_user: UpdateUserSchema = Depends(get_current_user),db:Session = Depends(get_db)):
    current_user.twitter = user_data.twitter
    current_user.telegram = user_data.telegram
    current_user.bio = user_data.bio
    current_user.photo = user_data.photo
    current_user.dnft = user_data.dnft
    current_user.dp = user_data.dp
    current_user = user_data.dict(exclude_unset=True)
    db.commit()
    return current_user
