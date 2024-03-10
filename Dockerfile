FROM python:3.12

ENV FASTAPI_ENV=production
ENV TZ=Europe/Moscow


COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./ /app

WORKDIR /app


# Выполняем миграцию для БД и запускаем  celery с проектом
CMD alembic upgrade head && \
    celery -A celery_config worker --loglevel=INFO --logfile=/var/log/celery_worker.log --pidfile=/var/run/celery_worker.pid & \
    celery -A celery_config beat --loglevel=INFO --logfile=/var/log/celery_beat.log --pidfile=/var/run/celery_beat.pid & \
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000