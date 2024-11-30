
from fastapi import HTTPException
from pydantic import ValidationError
from .modelsRequest import AddItem, DeleteItem

def validate_add_item(data: AddItem):
    if not all([data.id, data.classID, data.SystemInTime]):
        raise HTTPException(status_code=400, detail="Missing required fields in add_item request.")

def validate_delete_item(data: DeleteItem):
    if not all([data.id, data.classID, data.SystemOutTime]):
        raise HTTPException(status_code=400, detail="Missing required fields in delete_item request.")
