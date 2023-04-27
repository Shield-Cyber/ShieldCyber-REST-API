from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import logging
from app import LOGGING_PREFIX, USERNAME, PASSWORD

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.auth")

SECRET_KEY = "5ef48f2decbe7df5467a771018a2d33d05d4b8d896751d72cb80c71883c483f8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

users_db = {
    "admin": {
        "username": USERNAME,
        "hashed_password": CryptContext(schemes=["bcrypt"], deprecated="auto").hash(PASSWORD),
        "disabled": False,
    }
}

class Auth():

    class Token(BaseModel):
        access_token: str
        token_type: str

    class TokenData(BaseModel):
        username: str | None = None

    class User(BaseModel):
        username: str
        disabled: bool | None = None

    class UserInDB(User):
        hashed_password: str

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")

    def verify_password(plain_password, hashed_password):
        LOGGER.debug("Verfying Password")
        return Auth.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(password):
        LOGGER.debug("Getting Password Hash")
        return Auth.pwd_context.hash(password)

    def get_user(db, username: str):
        LOGGER.debug(f"Getting User '{username}' from Database")
        if username in db:
            user_dict = db[username]
            return Auth.UserInDB(**user_dict)

    def authenticate_user(users_db, username: str, password: str):
        LOGGER.debug("Authenticating User")
        user = Auth.get_user(users_db, username)
        if not user:
            LOGGER.debug(f"User '{username}' not found in Database.")
            return False
        if not Auth.verify_password(password, user.hashed_password):
            LOGGER.debug(f"User '{username}' password not correct.")
            return False
        return user

    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        LOGGER.debug("Creating Access Token")
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        LOGGER.debug("Access Token Created")
        return encoded_jwt

    async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
        LOGGER.debug("Getting Current User")
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                LOGGER.debug("Username is None")
                raise credentials_exception
            token_data = Auth.TokenData(username=username)
        except JWTError as err:
            LOGGER.debug(f"JWT Error: {err}")
            raise credentials_exception
        user = Auth.get_user(users_db, username=token_data.username)
        if user is None:
            LOGGER.debug("User is None")
            raise credentials_exception
        return user

    async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
    ):
        LOGGER.debug("Getting Current Active User")
        if current_user.disabled:
            LOGGER.debug("User Disabled")
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user