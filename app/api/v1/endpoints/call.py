import logging


from fastapi import APIRouter
from app.utils.email.smtp_server import email_sender

from app.core.config import settings
from app.utils.email.template_renderer import render_template
router = APIRouter(tags=['call'])


logger = logging.getLogger(__name__)


@router.get("/order_call/")
async def search(phone: str, name: str):

    context = {
        "user_phone": phone,
        "name": name
    }

    html_content = render_template(settings.template.ORDER_CALL, context)
    # Отправка письма с подтверждением
    await email_sender.send_email(
        email_to=settings.email.MANAGER_EMAIL,
        subject='Пользователь сделал заказ',
        body=html_content
    )
    return {"message": "Письмо менеджеру отправлено"}