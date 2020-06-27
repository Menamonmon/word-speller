import requests

def make_dict_request(word, api_key, req_url):
	return requests.get(f"{req_url}{word}?key={api_key}").json()

def get_definition(json, def_keyword='shortdef'):
	if isinstance(json, list):
		json = json[0]
	
	if def_keyword not in json:
		present, val = get_property(json, def_keyword)
		if present:
			return val

		raise Exception("JSON not in format")

	return json[def_keyword][0]

def get_property(json, prop_name):
	# makes sure that the json argument is a list or a dict to avoid interpeting a str as a list
	if not (isinstance(json, dict) or isinstance(json, list)):
		return False, None

	# checks if the prop_name is not in the json to decide if it's going to do a depth search
	if prop_name not in json:
		# formatting the values according to their type
		if isinstance(json, dict):
			values = json.values()
		elif isinstance(json, list):
			values = json
		else:
			values = []

		# iterating through the members of each field and applying the method recursively on them.
		for value in values:
			found, val = get_property(value, prop_name)
			if found:
				# ending the recursion if the value if found
				return True, val

		# returning false & none if when the recursion ends with no value found.
		return False, None

	# returning the values if it's in the first level.
	return True, json[prop_name]