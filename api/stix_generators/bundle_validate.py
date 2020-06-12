"""

STIX2 Bundle Generator

"""

import validators
from stix2 import File


class BundleValidate():
	"""
	Validate incoming custom bundle requests
	by ensuring correct format and successful...
	"""

	def __init__(self, data=None):
		self.data = [self.sift_dictionary(obj) for obj in data]
		self.response = {"valid":True}
		self.validation_map = {
            "IPv4 Address": self.validate_ipv4,
            "Domain Name": self.validate_domain_name,
            "MAC Address": self.validate_mac,
            "URL": self.validate_url,
            "File": self.validate_file
		}

		print("data in BundleValidate:", self.data)
		if data is not None:
			self.validate()


	def get_response(self):
		return self.response


	def validate(self):
		for custom_sdo in self.data:
			sdo_key = list(custom_sdo.keys())[0]
			if sdo_key in self.validation_map.keys():
				if custom_sdo[sdo_key] == {}:
					pass
				else:
					validation_function = self.validation_map.get(sdo_key)
					is_valid, response = validation_function(custom_sdo[sdo_key])
					if not is_valid:
						self.response["valid"] = False
						self.response[sdo_key] = {"msg":response}

		print(f"[STIX2 VALIDATE] VALIDATION COMPLETE")


	def validate_ipv4(self, value):
		if validators.ipv4(value["value"]):
			return True, ""
		else:
			return False, "Invalid IPv4 format"


	def sift_dictionary(self, data):
		return_dict = {}
		for key, value in data.items():
			if type(value) is dict:
				return_dict[key] = self.sift_dictionary(value)
			else:
				if value == "":
					continue
				return_dict[key] = value
		return return_dict


	def validate_domain_name(self, value):
		if validators.domain(value["value"]):
			return True, ""
		else:
			return False, "Invalid domain name format"


	def validate_url(self, value):
		if validators.url(value["value"]):
			return True, ""
		else:
			return False, "Invalid URL format"


	def validate_mac(self, value):
		if validators.mac_address(value["value"]):
			return True, ""
		else:
			return False, "Invalid MAC address format"


	def validate_file(self, value):
		keys = list(value.keys())
		if "encoding" not in keys and "hashes" not in keys:
			return True, ""
		elif "encoding" in keys:
			if value["encoding"] not in ["MD5", "SHA-1", "SHA-256"] or ("encoding" not in keys and "hashes" not in keys):
				return False, "Invalid hash encoding selection... Please choose MD5, SHA-1, or SHA-256"
		elif "hashes" in keys and "encoding" in keys:
			try:
				File(name=value["name", hashes={value["encoding"]:value["hashes"]}])
			except Exception as e:
				return False, e




