import logging
import json
import azure.functions as func
from .extractor import extract
import os

# Azure function which accepts a URL parameter to convert files using libreoffice
# YAGNI for anything else...
def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    extraction_result = extract(request=req)
    return extraction_result