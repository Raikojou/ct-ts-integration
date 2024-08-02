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
        piecesweight = tile_data['weight']
        selling_unit = tile_data['sellingunit']     # this is irrelevant, for anything other than sqm has to see piecesm2. if piecesm2 = 0, treat as pieces.
        if tile_data['hasshades'] == True:
            shades = [
                {
                    "shade": loc['shade'].split('*')[0],
                    "available in pieces": available,
                    "available in sqm": round(available / piecesm2, 4) if selling_unit == "SQM" else None,
                    "info pieces / box": pcsbox,
                    "info m2 / box": round(pcsbox / piecesm2, 4) if selling_unit == "SQM" else None,
                    "info weight per box in kg": pcsbox * piecesweight
                }
                for loc in locations
                for available, pcsbox in [(loc['available'], loc['pcsbox'])]
            ]
        else:
            shades = tile_data['available']

        backorder = [
            {
                "quantity ordered (unit is according to selling unit)": data['Qty'],
                "date expected": data['Date']
            } for data in eta_data
        ]

        output = {
            'name': name,
            'pieces/m2': piecesm2,
            'weight per piece (in kg)': piecesweight,
            'quantity Available': shades,
            'backorder': backorder,
            'selling unit': selling_unit
        }
        if name == None:
            return jsonify({"error": "empty payload"})
        else:
            print(output)
            return jsonify(output)
        
    except KeyError as e:
        return jsonify({"error": f"Missing key in response data: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500