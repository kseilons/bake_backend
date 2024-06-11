from logging import getLogger
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions, models, schemas

from .models import User
from .utils import get_user_db
from app.core.config import settings

from app.utils.email.smtp_server import email_sender
from app.utils.email.template_renderer import render_template

SECRET = settings.auth.SECRET
logger = getLogger()


class UserManager(UUIDIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
        
    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        forgot_pass_link = settings.FRONTEND_URL + settings.auth.FORGOT_PASSWORD_PATH + token
        html_content = render_template('forgot_password.html', {'forgot_pass_link': forgot_pass_link})
        logger.debug(f"Send latter to {user.email}")
        # Отправка письма с подтверждением
        await email_sender.send_email(
            email_to=user.email,
            subject='Подтвердите свою почту',
            body=html_content
        )
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        confirmation_link = settings.FRONTEND_URL+ settings.auth.VERIFY_PATH + token
        html_content = render_template('email_confirm.html', {'confirmation_link': confirmation_link})
        logger.debug(f"Send latter to {user.email}")
        # Отправка письма с подтверждением
        await email_sender.send_email(
            email_to=user.email,
            subject='Подтвердите свою почту',
            body=html_content
        )
    
        logger.info(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)