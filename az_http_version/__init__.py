import logging
import json
import azure.functions as func
import os

# Azure function which accepts a URL parameter to convert files using libreoffice
# YAGNI for anything else...
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    version = "v-dev-0.02"
    return func.HttpResponse(json.dumps({"version": version}), status_code=200, mimetype="application/json")    