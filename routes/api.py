from flask import Blueprint, request, jsonify
import numpy as np


api_bp = Blueprint("api", __name__)


@api_bp.route("/upload")
def upload():
    return jsonify({
        "status": True
    })
