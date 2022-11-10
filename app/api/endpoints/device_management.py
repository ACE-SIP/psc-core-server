import json
import os
from bson import json_util
from fastapi import APIRouter, Depends
from app.api import oauth2
from app.api.models.Ubibot import DeviceRegIn
from app.api.models.User import User, get_current_active_user
from db.mongo_client import Database


router = APIRouter(responses={404: {"description": "Device Not found"}})


@router.post('/register')
def register_device(device: DeviceRegIn, token: str = Depends(oauth2)):
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_DEVICE_MGT')]
    query = {"channel_id": device.channel_id, "product_id": device.product_id, "serial": device.serial,
             "ssid_base64": device.ssid_base64, "valid_from": device.valid_from, "expire_until": device.expire_until}
    results = collection.find(query)
    if len(json.loads(json_util.dumps(results))) > 0:
        return "Device Already Exist!"
    rsp = collection.insert_one(query)
    if rsp.inserted_id is not None:
        return "SUCCESS"
    return "ERROR"


@router.get('/all')
def list_all_devices(current_user: User = Depends(get_current_active_user)):
    print("Current user: {}".format(current_user))
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_DEVICE_MGT')]
    return json.loads(json_util.dumps(collection.find()))


@router.get('/select/{query_type}/value/{query_type_value}')
def query_by_id(query_type, query_type_value, current_user: User = Depends(get_current_active_user)):
    print("Current user: {}".format(current_user))
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_DEVICE_MGT')]
    query = {query_type: query_type_value}
    return json.loads(json_util.dumps(collection.find(query)))


@router.get('/delete/{query_type}/value/{query_type_value}')
def delete_by_id(query_type, query_type_value, current_user: User = Depends(get_current_active_user)):
    print("Current user: {}".format(current_user))
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_DEVICE_MGT')]
    query = {query_type: query_type_value}
    rsp = collection.delete_one(query)
    return "DELETE SUCCESS" if rsp.deleted_count == 1 else "FAIL TO DELETE or DEVICE NOT EXIST"
