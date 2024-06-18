from re import template
import uuid
from fastapi import APIRouter
from app.auth.schemas import IUser, IUserCreate
from app.utils.email.smtp_server import EmailSender
from app.auth.auth import auth_backend
from app.auth.auth import fastapi_users

router = APIRouter(tags=['auth'])

email_sender = EmailSender()


router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/jwt"
)
router.include_router(fastapi_users.get_register_router(IUser, IUserCreate))

router.include_router(fastapi_users.get_verify_router(IUser))

router.include_router(fastapi_users.get_reset_password_router())