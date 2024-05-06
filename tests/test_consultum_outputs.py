import unittest
import json
from mocker import create_mock_request, get_response
from pathlib import Path
import os
from os import listdir
from pprint import pprint
from utils.helpers import write_json

kTestInputsDirectory = 'consultum_sample_inputs'
kTestOutputsDirectory = 'consultum_sample_outputs'

class TestFunction(unittest.TestCase):
    def test_consultum(self):
        # self.assertEqual(first='a', second='a')
        """
        Run tests with:  python3 -m unittest discover tests
        """
        # set maxDiff as None for visual debugging
        self.maxDiff = None
        
        # get list of test inputs
        script_location = Path(__file__).absolute().parent
        sample_inputs_location = script_location / kTestInputsDirectory
        
        sample_inputs = list()
        for file in os.listdir(sample_inputs_location):
            pprint(file)
            if file.endswith("doc"):
                sample_inputs.append(os.path.join(sample_inputs_location, file))
        
        # loop over each sample input, assert against sample output
        # assumes a simple file naming convention: "input_01.pdf" -> "output_01.json"
        for test_input_location in sample_inputs:
            # construct a mock HTTP request
            # req = create_mock_request(filepath="./tests/sample_inputs/input_01.pdf")
            
            headers = {'x-planpod-dealer-group': 'consultum'}
            req = create_mock_request(filepath=test_input_location, headers=headers)

            # get response for this mock HTTP request
            resp = get_response(req)
            # define the expected result and set the request_id to None
            # open and parse JSON   
            test_output_file_name = os.path.basename(test_input_location)
            test_output_file_name += ".json"
            test_output_location = script_location / kTestOutputsDirectory / test_output_file_name
            with open(test_output_location) as f:
                expected_result = json.load(f)
                expected_result = expected_result['data']

            # pprint(resp)            
            # print('------------------------------------------------------------')
            # print('------------------------------------------------------------')
            # print('------------------------------------------------------------')
            # pprint("resp['data'] = ")
            # pprint(resp['data'])
            write_json('', resp['data'], 'output-server.json')
            # print('------------------------------------------------------------')
            # print('------------------------------------------------------------')
            # print('------------------------------------------------------------')
            # pprint("expected_result = ")
            # pprint(expected_result)
            write_json('', expected_result, 'output-hardcoded.json')
            # print('------------------------------------------------------------')
            # print('------------------------------------------------------------')
            # print('------------------------------------------------------------')
            # # check the output
            print(f"Running assertDictEqual for input: {test_input_location}")
            self.assertDictEqual(resp['data'], expected_result)