import base64
import json
import os
import numpy as np
import requests

from app.blockchain.account import get_account_by_participant
from app.blockchain.integration import send_transaction
from db.mongo_client import Database


async def detect_anomaly(results):
    temperatures = results['temperature']
    humidities = results['humidity']
    ambient_light = results['ambient_light']
    anomaly_detected = {}
    if np.average(temperatures) > 25:
        # save anomaly data to blockchain
        anomaly_detected['temperature'] = "temperature must not greater than 25"
    if np.average(humidities) > 57:
        # save anomaly data to blockchain
        anomaly_detected['humidity'] = "humidity must not greater than 57"
    if np.average(ambient_light) > 52:
        # save anomaly data to blockchain
        anomaly_detected['ambient_light'] = "ambient light must not greater than 52"
    if anomaly_detected:
        private_key, my_address = get_account_by_participant('PHRASE_ROOT')
        note = json.dumps(anomaly_detected).encode()
        # send data to tx
        tx_id = send_transaction(private_key, my_address, note)
        anomaly = {"anomaly": anomaly_detected,
                   "tx_id": tx_id,
                   "inserted_id": results['inserted_id']}
        collection_anomaly = Database.DATABASE[os.environ.get('DB_COLLECTION_ANOMALY')]
        collection_anomaly.insert_one(anomaly)
    print("Complete Anomaly Detection")


if __name__ == '__main__':
    tx_id = "MQ667TET6H63X33236WDWG4BFXAV64QBQS6DKGM4GD4B6ZIF2VRQ"
    api_url = 'https://algoindexer.testnet.algoexplorerapi.io/v2/transactions/{}'.format(tx_id)
    response = requests.get(api_url)
    json_response = json.loads(response.text)
    note = json_response['transaction']['note']
    print(note)
    print("Decoded note: {}".format(base64.b64decode(note).decode()))
