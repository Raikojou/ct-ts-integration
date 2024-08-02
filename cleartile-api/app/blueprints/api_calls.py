import requests
from ..config import Config

base_url = "api.stoneworld.com.au/api/WebServices/v3.0/"

def GetTileCatalogItem(state, sku):
    url = f'https://{state}{base_url}GetTileCatalogItem?id={sku}'
    header = {
        'authorization': Config.API_KEYS.get(state.lower())
    }
    response = requests.get(url, headers=header)
    return response.json()

def ReturnItemETA(state, sku):
    url = f'https://{state}{base_url}ReturnItemETA?itemCode={sku}'
    header = {
        'authorization': Config.API_KEYS.get(state.lower())
    }
    response = requests.get(url, headers=header)
    return response.json()