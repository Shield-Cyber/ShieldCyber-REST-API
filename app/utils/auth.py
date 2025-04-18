from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from pydantic import BaseModel
import logging
from app import LOGGING_PREFIX, USERNAME, PASSWORD
from app.database import crud as DATABASE
import pickle
import secrets

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.auth")

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

read_db = DATABASE.read("users")

if read_db == None:
    LOGGER.warn("Users Database not Found.")
    temp_db = {
        "admin": {
            "username": USERNAME,
            "password": PASSWORD,
            "hashed_password": bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt()),
            "disabled": False,
        }
    }
    DATABASE.create("users", pickle.dumps(temp_db))
    temp_db = None
    LOGGER.info("Users Database Created.")
    users_db: dict = pickle.loads(DATABASE.read("users"))
else:
    LOGGER.info("Users Database Found.")
    users_db: dict = pickle.loads(DATABASE.read("users"))

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

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")

    def verify_password(plain_password, hashed_password):
        LOGGER.debug("Verfying Password")
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def get_password_hash(password):
        LOGGER.debug("Getting Password Hash")
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # I hate this, its terrible and it should be changed to make something actually secure and not stupid.
    def get_admin_password():
        LOGGER.debug("Getting Cleartext Admin Password: This is a bad practice, please change this in the future.\nThis is only used for API endpoints to connect to the OpenVAS Scanner. Until I make a better solution this is what we got.")
        return users_db["admin"]["password"]

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
