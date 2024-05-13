FROM python:3.12

ENV FASTAPI_ENV=production
ENV TZ=Europe/Moscow


COPY /app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./ /app

WORKDIR /app


# Выполняем миграцию для БД и запускаем  celery с проектом
CMD alembic upgrade head && \
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000