import json

class ExtractionResult:
    def __init__(self, request_id):
        self.request_id = request_id
        self.success = False
        self.error = None
        self.data = None

    def to_json(self):
        return json.dumps(self.__dict__)
