import getopt
import json
import sys
import copy

def process_ri(json_data: dict):
	try:
		objectives = []
		for d in json_data['goals_needs']:
			c_data = {}
			try:
				c_data['adviceArea'] = d['Advice area']
				c_data['title'] = d['Description'].split("\n")[0]
				c_data['description'] = "\n".join(d['Description'].split("\n")[1:]).strip()
				c_data['needsAttention'] = False
			except:
				c_data['needsAttention'] = True
			objectives.append(c_data)
			
		scopeOfAdvice = []
		for d in json_data['scope_of_advice']:
			c_data = {}
			try:
				c_data['adviceArea'] = d['advice_area'].strip()
				c_data['scope'] = d['relevant_scope'].replace("+","").replace(" ","")
				c_data['explanation'] = d['explanation'].strip()
				c_data['needsAttention'] = False
			except:
				c_data['needsAttention'] = True
			scopeOfAdvice.append(c_data)

		scopeOfAdviceDetails = []
		scopeOfAdviceDetailsKeys = ['scope_of_advice_insurance','scope_of_advice_superannuation','scope_of_advice_retirement_income','scope_of_advice_estate_planning','scope_of_advice_investment','scope_of_advice_cash_flow_management','scope_of_advice_aged_care','scope_of_advice_social_security','scope_of_advice_debt_management']
		scopeOfAdviceDetailsValues = ['Insurance','Superannuation','Retirement Income','Estate Planning','Investment','Cash flow management','Advice aged care','Social Security','Debt management']
		for index,key in enumerate(scopeOfAdviceDetailsKeys):
			subAreas = []
			scope_data = {}
			for d in json_data[key]:
				c_data = {}
				try:
					c_data['subAdviceArea'] = d['Sub-Advice Area'].strip()
					c_data['inOut'] = d['In/Out']
					c_data['explanation'] = d['explanation'].strip()
					c_data['needsAttention'] = False
				except:
					c_data['needsAttention'] = True
				subAreas.append(c_data)
			scope_data['adviceArea'] = scopeOfAdviceDetailsValues[index]
			scope_data['subAreas'] = subAreas
			scopeOfAdviceDetails.append(scope_data)

		personalProfile = {}
		personalProfile['employmentDetails'] = json_data['employment_details']
		personalProfile['retirementDetails'] = json_data['retirement_details']
		personalProfile['investorProfileDetails'] = json_data['investor_profile_details']
		personalProfile['personalDetails'] = json_data['personal_profile']['personal_details']
		personalProfile['contactDetails'] = json_data['personal_profile']['contact_details']
		personalProfile['childrenAndDependantDetails'] = json_data['personal_profile']['children_and_dependant_details']
		personalProfile['healthDetails'] = json_data['personal_profile']['health_details']

		attributes = {}
		attributes['seekingAdvicePurpose']=json_data['seeking_advice_purpose']
		attributes['futureSituationChange']=json_data['future_situation_change']
		attributes['objectives']=objectives
		attributes['scopeOfAdvice']=scopeOfAdvice
		attributes['scopeOfAdviceDetails']=scopeOfAdviceDetails
		attributes['personalProfile']=personalProfile
  
		attributes['incomeDetails'] = json_data['income_details']
		attributes['expenditureDetails'] = json_data['expenditure_details']
		attributes['lifestyleDetails'] = json_data['lifestyle_details']
		attributes['superannuationPensionAndAnnuityDetails'] = json_data['superannuation_pension_and_annuity_details']
		attributes['liabilitiesDetails'] = json_data['liabilities_details']
		attributes['realEstateDetails'] = json_data['real_estate_details']
		attributes['estateDetails'] = json_data['estate_details']
		attributes['personalLifeInsurance'] = json_data['personal_lifeinsurance']
		attributes['incomeProtection'] = json_data['income_protection']

		data={}
		data['type']='factfindData'
		data['attributes']=attributes
  
		return None, data
	except Exception as e:
		template = "An exception of type {0} occurred. Arguments:\n{1!r}"
		message = template.format(type(e).__name__, e.args)
		print(message)
		return message, None


def process_consultum(json_data: dict):
	return None, json_data

def process(dealer_group_id, json_data: dict):
	
	# process based on DG
	if dealer_group_id == "ri":
		# RI
		error, data = process_ri(json_data=json_data)
	elif dealer_group_id == "consultum":
		# consultum
		error, data = process_consultum(json_data=json_data)
	if error is not None:
		return error, None    
	try:
		# convert all keys to camelcase, recursively

		data = convert_dict_to_camelcase(in_dict=copy.deepcopy(data))
		# replace required keys
		data = replace_keys(in_dict=copy.deepcopy(data))
	
		return None, data
	except Exception as e:
		template = "An exception of type {0} occurred. Arguments:\n{1!r}"
		message = template.format(type(e).__name__, e.args)
		print(message)
		return message, None

def replaced_key(key: str):
	key_replacement_dict = {
		'amount(GrossPa)': 'amount',
		'investmentType/Name': 'investmentType',
		'amountOwing': 'amount',
		'amount(Pa)': 'amount',
		'dateOfBirth': 'dateofbirth',
		'repaymentAmt/Freq': 'repaymentAmt',
		'policyNo.': 'policyNo',
		'life&Amount': 'lifeAmount',
		'standAlone?': 'standAlone',
		'buyBack?': 'buyBack',
		'reinstatement?': 'reinstatement'
	}
	return key_replacement_dict.get(key, key)

def replace_keys(in_dict: dict):
	result = dict() 
	for key in in_dict.keys():
		# recursively process key-value pairs
		if isinstance(in_dict[key], dict): 
			result[replaced_key(key)] = replace_keys(in_dict[key]) 
		elif isinstance(in_dict[key], list): 
			list_of_dicts = in_dict[key]
			result[replaced_key(key)] = [replace_keys(item) for item in list_of_dicts]
		else: 
			result[replaced_key(key)] = in_dict[key] 
	return result    
		
def convert_dict_to_camelcase(in_dict: dict):
	result = dict() 
	for key in in_dict.keys():
		# recursively process key-value pairs
		if isinstance(in_dict[key], dict): 
			result[to_camel_case(in_snake_str=key)] = convert_dict_to_camelcase(in_dict[key]) 
		elif isinstance(in_dict[key], list): 
			list_of_dicts = in_dict[key]
			result[to_camel_case(in_snake_str=key)] = [convert_dict_to_camelcase(item) for item in list_of_dicts]
		else:
			# trim whitespace if string
			original_val = in_dict[key]
			new_val = original_val.strip() if isinstance(original_val, str) else original_val
			result[to_camel_case(in_snake_str=key)] = new_val
 
	return result

def make_first_character_lowercase(in_string: str):
	return in_string[0].lower() + in_string[1:]

def to_camel_case(in_snake_str: str):
	in_snake_str = in_snake_str.replace(" ", "_")
	lower_case_string = make_first_character_lowercase(in_string=in_snake_str)
	components = lower_case_string.split('_')
	# We capitalize the first letter of each component except the first one
	# with the 'title' method and join them together.
	result = components[0] + ''.join(x.title() for x in components[1:])
	return result

def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('test.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('test.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	print('Input file is ' + inputfile)
	print('Output file is ' + outputfile)
   
	with open(inputfile) as f:
		json_data = json.loads(f.read())
  
	error, processed_text = process(json_data=json_data)
	if error is None:
		with open(outputfile, "w") as outfile:
			json.dump(processed_text, outfile, indent=4)
	else:
		print("Error processing text: " + str(error))
  
if __name__ == "__main__":
   main(sys.argv[1:])