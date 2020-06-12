def sift_dictionary(data):
	return_dict = {}
	for key, value in data.items():
		if type(value) is dict:
			return_dict[key] = sift_dictionary(value)
		else:
			if value == "":
				continue
			return_dict[key] = value
	return return_dict
