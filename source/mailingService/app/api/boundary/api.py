import logging
from fastapi import APIRouter, Request

from api.control.api_bf import ApiBf
from entity.models.mail_data import MailUpdateData, MailErrorData
from entity.enums.action import Action

api_router = APIRouter()
api_bf = ApiBf()

@api_router.post("/send_update_mail")
async def send_update_mail(request: list[MailUpdateData]):
    return await api_bf.prepare_mailing_data(request, Action.CHANGED)

@api_router.post("/send_error_mail")
async def send_error_mail(request: MailErrorData):
    return await api_bf.prepare_mailing_data_error(request)
