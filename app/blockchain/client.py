from algosdk.v2client import algod
from algosdk.kmd import KMDClient


def get_algod_client():
    """Instantiate and return Algod client object."""
    algo_address = "http://203.101.228.152:4001"
    algo_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    return algod.AlgodClient(algo_token, algo_address)


def get_kmd_client():
    """Instantiate and return KMD Client object."""
    algo_address = "http://203.101.228.152:4002"
    algo_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    return KMDClient(algo_token, algo_address)
