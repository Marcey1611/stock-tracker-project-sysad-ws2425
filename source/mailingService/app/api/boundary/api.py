import logging
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from api.control.api_bf import ApiBf
from api.validation.validator import Validator

api_router = APIRouter()
api_bf = ApiBf()
validator = Validator()

@api_router.post("/send_update_mail")
async def send_update_mail(request: Request):
    request_data = await request.json()
    valid_data, action = validator.validate_data(request_data)
    return await api_bf.prepare_mailing_data(valid_data, action)

@api_router.post("/send_error_mail")
async def send_error_mail(request: Request):
    request_data = await request.json()
    valid_data = validator.validate_error_message(request_data)
    return await api_bf.prepare_mailing_data_error(valid_data)
