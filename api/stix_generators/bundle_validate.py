"""

STIX2 Bundle Generator

"""

import validators
from stix2 import File
from .stix_utils.utils import sift_dictionary


class BundleValidate():
	"""
	Validate incoming custom bundle requests
	by ensuring correct format and successful...
	"""

	def __init__(self, data=None):
		self.data = [sift_dictionary(obj) for obj in data]
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
				print(custom_sdo)
				print(custom_sdo[sdo_key])
				if custom_sdo[sdo_key] == {}:
					pass
				else:
					validation_function = self.validation_map.get(sdo_key)
					is_valid, response = validation_function(custom_sdo[sdo_key])
					if not is_valid:
						self.response["valid"] = False
						self.response[sdo_key] = {"msg":response}

		print(f"[STIX2 VALIDATE] VALIDATION COMPLETE")
		print(self.response)


	def validate_ipv4(self, value):
		if validators.ipv4(value["value"]):
			return True, ""
		else:
			return False, "Invalid IPv4 format"


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
		valid_encodings = ["MD5", "SHA-1", "SHA-256"]

		if "encoding" not in keys and "hashes" not in keys:
			return True, ""

		if value["encoding"] not in valid_encodings or ("encoding" not in keys and "hashes" in keys):
			return False, "Invalid encoding selection... Please choose SHA-1, SHA-256, or MD5"

		else:
			try:
				File(name="", hashes={value["encoding"]:value["hashes"]})
				return True, ""
			except Exception as e:
				print(e)
				return False, str(e)
