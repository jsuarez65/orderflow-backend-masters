from typing import Any
from flask import jsonify, Response


def apiResponse(
    message: str,
    data: Any = None,
    success: bool = True,
    status: int = 200
) -> tuple[Response, int]:
    
    return jsonify({
        "success": success,
        "message": message,
        "data": data
    }), status