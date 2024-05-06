import logging
import json
import azure.functions as az_func

class RequestUtils:
    @staticmethod
    def api_response(func):
        def inner1(*args, **kwargs):
            try:
                code, obj = func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Unable to complete request, reason: {e}")
                logging.exception(e)
                err = {
                    "error": {
                        "title": "Unable to complete request",
                        "status": "500",
                        "detail": str(e)
                    }
                }
                return az_func.HttpResponse(
                    json.dumps(err),
                    headers= {
                        "Content-Type": "application/json"
                    },
                    status_code=500
                )
            return az_func.HttpResponse(
                json.dumps(obj),
                headers= {
                    "Content-Type": "application/json"
                },
                status_code=code
            )
        return inner1

    @staticmethod
    def html_response(func):
        def inner1(*args, **kwargs):
            try:
                code, obj = func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Unable to complete request, reason: {e}")
                logging.exception(e)
                err = {
                    "error": {
                        "title": "Unable to complete request",
                        "status": "500",
                        "detail": str(e)
                    }
                }
                return az_func.HttpResponse(
                    json.dumps(err),
                    headers= {
                        "Content-Type": "application/json"
                    },
                    status_code=500
                )
            return az_func.HttpResponse(
                obj,
                headers= {
                    "Content-Type": "text/html"
                },
                status_code=code
            )
        return inner1