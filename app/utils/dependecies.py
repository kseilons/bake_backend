from sqlalchemy.orm import Session

from app.crud import users as users_controller
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models.database import get_db
from app.schemas.users import User 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    user = await users_controller.get_user_by_token(token, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def verify_admin_user(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not authorized to perform this action"
        )