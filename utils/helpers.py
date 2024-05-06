import os
import datetime
import json

def logging_enabled():
	return os.environ.get('DEBUG_LOGGING', False)

def write_json(file_prefix, data_dict, filename=None):
	# writes content to file in folder from get_output_dir with filename:
	# {{file_prefix}}_%m-%d-%y %H:%M:%S.json
	if filename is None:
		now = datetime.datetime.now()
		now = now.strftime('%m-%d-%y_%H-%M-%S')
		filename = file_prefix + '_' + now + '.json'
	
	cwd = os.path.abspath(os.getcwd())
	filepath = os.path.join(cwd, filename)
	with open(filepath, 'w') as outfile:
		json.dump(data_dict, outfile, indent=4)
	return filename