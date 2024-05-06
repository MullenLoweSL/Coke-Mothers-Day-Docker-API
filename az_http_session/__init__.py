import logging
import json
import uuid
import azure.functions as func
from ..models.SessionModel import SessionModel
from controllers import SessionController

handler = SessionController()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request!')

    # Handle POST
    if req.method == "POST":
        try:
            # save IP
            x_forwarded_for = req.headers.get('X-Forwarded-For')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                try:
                    ip_address = req.remote_addr  # Use remote_addr if 'X-Forwarded-For' is not set
                except AttributeError:
                    # this must be localhost, set LOCALHOST as IP
                    ip_address = "LOCALHOST"

            # add IP address to payload
            payload = {}
            payload["ip_address"] = ip_address
            payload["id"] = str(uuid.uuid4())
            result = SessionModel(**payload)
            return handler.post_session(result)
        except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            return func.HttpResponse(json.dumps({"error": message}), status_code=400)
    elif req.method == "PATCH":
        data: str = req.params.get("data")
        session_id: str = req.route_params.get('session_id')
        req_body = req.get_json()
        return handler.patch_session(session_id, data, req_body)
        
            
    return func.HttpResponse(json.dumps({"error": "Unknown HTTP action requested."}), status_code=400)