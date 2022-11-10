from pydantic import BaseModel
from typing import List, Union
from datetime import datetime


class DeviceRegIn(BaseModel):
    channel_id: str
    product_id: str
    serial: str
    ssid_base64: str
    valid_from: datetime
    expire_until: datetime


class DataRecordIn(BaseModel):
    channel_id: str
    product_id: str
    serial: str
    feeds: List[object] = []
    cali: object = {}
    status: str
    ssid_base64: str

