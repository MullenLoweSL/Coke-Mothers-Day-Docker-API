import logging
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.Logger.root.level = 10
    logging.debug("Debug message here")

    headers = dict(req.headers)
    return func.HttpResponse(json.dumps(headers), status_code=200, mimetype="application/json")