import logging


from fastapi import APIRouter
from app.auth.schemas import IOrderPhone
from app.utils.email.smtp_server import email_sender

from app.core.config import settings
from app.utils.email.template_renderer import render_template
router = APIRouter(tags=['call'])


logger = logging.getLogger(__name__)


@router.post("/order_call/")
async def search(data: IOrderPhone):

    context = {
        "user_phone": data.phone,
        "name": data.name
    }

    html_content = render_template(settings.template.ORDER_CALL, context)
    # Отправка письма с подтверждением
    await email_sender.send_email(
        email_to=settings.email.MANAGER_EMAIL,
        subject='Пользователь сделал заказ',
        body=html_content
    )
    return {"message": "Письмо менеджеру отправлено"}