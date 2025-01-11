import logging
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from api.control.api_bf import ApiBf
from api.validation.validator import Validator
from entity.enums.action import Action

api_router = APIRouter()
api_bf = ApiBf()
validator = Validator()

@api_router.post("/send_mail_added")
async def send_mail_added(request: Request):
    request_data = await request.json()
    valid_data = validator.validate_data(request_data)
    return await api_bf.prepare_mailing_data(valid_data, Action.ADDED)

@api_router.post("/send_mail_deleted")
async def send_mail_deleted(request: Request):
    request_data = await request.json()
    valid_data = validator.validate_data(request_data)
    return await api_bf.prepare_mailing_data(valid_data, Action.DELETED)

@api_router.post("/send_error_mail")
async def send_error_mail(request: Request):
    request_data = await request.json()
    valid_data = validator.validate_error_message(request_data)
    return await api_bf.prepare_mailing_data_error(valid_data)
