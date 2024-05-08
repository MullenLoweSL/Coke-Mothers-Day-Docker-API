import logging
import json
import azure.functions as func

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    version = "v-dev-0.16"
    return func.HttpResponse(json.dumps({"version": version}), status_code=200, mimetype="application/json")