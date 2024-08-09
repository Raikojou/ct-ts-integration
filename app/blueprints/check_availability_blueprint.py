from flask import Blueprint, jsonify, request
import requests
from . import api_calls
from ..config import Config


check_availability_bp = Blueprint('check_availability_bp', __name__)

@check_availability_bp.route('/', methods=['GET'])
def check_availability():
    state = request.args.get('state')
    sku = request.args.get('sku').upper()

    if not sku:
        return jsonify({"error": "SKU is required"}), 400
    if not state:
        return jsonify({"error": "State is required"}), 400
    if state.lower() not in Config.API_KEYS:
        return jsonify({"error": "Invalid state"}), 400
    
    try:
        tile_data = api_calls.GetTileCatalogItem(state, sku)
        eta_data = api_calls.ReturnItemETA(state, sku)
        name = tile_data['description']
        piecesm2 = tile_data['piecesm2']
        locations = tile_data['locations']
        piecesweight = round(tile_data['weight'], 2)

        
        additional_details = {
            item['name']: item['value']
            for item in tile_data['extradetails']['userdefinedvalues']
            if item['value'] is not ""
        }

        if tile_data['hasshades'] == True:
            shades = [
                {
                    "shade": loc['shade'].split('*')[0],
                    "pcsavail": available,
                    "sqmavail": round(available / piecesm2, 4) if piecesm2 else None,
                    "boxpallet": loc['boxpallet'],
                    "pcsbox": pcsbox,
                    "sqmbox": round(pcsbox / piecesm2, 4) if piecesm2 else None,
                    "boxweight": round(pcsbox * piecesweight, 2)
                }
                for loc in locations
                for available, pcsbox in [(loc['available'], loc['pcsbox'])]
            ]
        else:
            shades = tile_data['available']

        backorder = [
            {
                "backorderqty": data['Qty'],
                "backordereta": data['Date']
            } for data in eta_data
        ]

        output = {
            'sku': tile_data['code'],
            'sellingunit': tile_data['sellingunit'].lower(),
            'name': name,
            'pcssqm': piecesm2,
            'pcsweight': piecesweight,
            'available': shades,
            'backorder': backorder,
            'details': additional_details
        }
        if name == None:
            return jsonify({"error": "empty payload"})
        else:
            return jsonify(output)
        
    except KeyError as e:
        return jsonify({"error": f"Missing key in response data: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
