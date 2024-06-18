
import json
from logging import getLogger
import logging.config
import uvicorn


from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.api.v1.api import api_router
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse


with open("app/core/logging.conf") as file:
    config = json.load(file)
logging.config.dictConfig(config)
logger = getLogger()


app = FastAPI(title="Bake Backend App")
app.include_router(api_router)




# Благодаря этой функции клиент видит ошибки, происходящие на сервере, вместо "Internal server error"
@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Здесь можно указать список разрешенных доменов
    allow_credentials=True,
    allow_methods=["POST", "GET", "PATCH", "PUT", "DELETE"],
    allow_headers=["*"],
)