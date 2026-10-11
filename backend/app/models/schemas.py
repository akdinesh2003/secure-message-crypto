from pydantic import BaseModel
from typing import Optional

class EncodeRequest(BaseModel):
    message: str

class DecodeRequest(BaseModel):
    payload: str

class StatusResponse(BaseModel):
    status: str
