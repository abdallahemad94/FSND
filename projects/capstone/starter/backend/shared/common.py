from flask import jsonify
from json import JSONEncoder
from datetime import date, datetime
def get_success_response(data, msg='Request completed successfully'):
    return jsonify({
        "success": True,
        "status_code": 200,
        "data": data,
        "message": msg
    }), 200


def get_fail_response(status_code, msg='Sorry, an error ha occurred'):
    return jsonify({
        "success": False,
        "status_code": status_code,
        "message": msg
    }), status_code


class DateJSONEncoder(JSONEncoder):
    def default(self, obj):
        if type(obj) is date or type(obj) is datetime:
            return obj.isoformat()
        else:
            return super().default(self, obj)
