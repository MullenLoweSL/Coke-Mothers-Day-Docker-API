import json
import re
import azure.functions as func
from FactFindScraperFunction import main

def create_mock_request(filepath: str, headers: dict) -> func.HttpRequest:
    # create and return a mock HTTP request.
    # read the file into request body
    f = open(filepath, "rb")
    data = f.read()
    f.close()

    # create the HTTP request
    request = func.HttpRequest(
        method='POST',
        body=data,
        url='/api/FactFindScraperFunction',
        headers=headers,
        params={'version': "2"})

    return request


def get_response(req: func.HttpRequest) -> func.HttpResponse:
    # call the function
    resp = main(req, None)
    # https://stackoverflow.com/questions/41129396/python-json-lower-case-nan
    # issue with lower case nan?
    resp = json.loads(resp)
    return resp
