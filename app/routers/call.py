import logging
from typing import List

from app.crud.categories import get_category_id
from app.schemas import products as schemas
from app.crud import products as controller
from app.models.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.schemas.users import User
from app.utils.dependecies import verify_admin_user
from app.utils.email.smtp_server import email_sender

from app.setting import manager_email
from app.utils.email.template_renderer import render_template
router = APIRouter(tags=['call'])


logger = logging.getLogger(__name__)


@router.get("/order_call/")
async def search(phone: str, name: str):

    context = {
        "user_phone": phone,
        "name": name
    }

    html_content = render_template('order_call.html', context)
    # Отправка письма с подтверждением
    await email_sender.send_email(
        email_to=manager_email,
        subject='Пользователь сделал заказ',
        body=html_content
    )
    return {"message": "Письмо менеджеру отправлено"}