from flask import Blueprint, jsonify
from src.api import call_definition_api

define_bp = Blueprint("define", __name__)

# test using http://localhost:8080/define/soup
@define_bp.route("/define/<word>")
def define(word):
    result = call_definition_api(word)
    # Handle error case (error message, status_code)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify(result)