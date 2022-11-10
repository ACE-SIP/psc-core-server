import os
from bson import json_util
from fastapi import APIRouter, Depends
from app.anomaly.detection import detect_anomaly
from app.api.models.Ubibot import DataRecordIn
from app.api.models.User import User, get_current_active_user
from db.mongo_client import Database
import json

router = APIRouter(responses={404: {"description": "Device Not found"}})


@router.get('/records/{source}')
def list_all_records_from_data_source(source, current_user: User = Depends(get_current_active_user)):
    print("Current user: {}".format(current_user))
    Database.initialize()
    collection = 'DB_COLLECTION_' + source.upper()
    collection = Database.DATABASE[os.environ.get(collection)]
    return json.loads(json_util.dumps(collection.find()))


@router.post('/forwarding')
async def receiving_records_from_registered_devices(item: DataRecordIn):
    Database.initialize()
    collection = Database.DATABASE[os.environ.get('DB_COLLECTION_DEVICE')]
    config = json.load(open(os.environ.get('BASE_CONFIG')))
    field_mapper = config['field_mapper']
    results = config['response']
    results['product_id'] = item.product_id
    results['serial'] = item.serial
    results['ssid_base64'] = item.ssid_base64
    results['channel_id'] = item.channel_id
    results['status'] = item.status
    for feed in item.feeds:
        field_key = list(feed.keys())[1]
        if field_key in list(field_mapper.keys()):
            results[field_mapper[field_key]].append(feed[field_key])
            if feed['created_at'] not in results['created_at']:
                results['created_at'].append(feed['created_at'])
    # Check anomaly data
    rsp = collection.insert_one(results)
    if rsp.inserted_id is not None:
        del results['_id']
        results['inserted_id'] = str(rsp.inserted_id)
        await detect_anomaly(results)
        return "SUCCESS"
    return "ERROR"
