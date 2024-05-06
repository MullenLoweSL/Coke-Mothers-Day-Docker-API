import random
import os
import json

class FileUtils:
    @staticmethod
    def read_json(file_path):
        # Open and read the JSON file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data