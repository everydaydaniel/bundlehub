"""

STIX2 RANDOM UTILS

"""

from random import randint
import utils
import re
import rstr

HASHES_REGEX = {  "MD5": ("^[a-fA-F0-9]{32}$", "MD5"),
    # "MD6": ("^[a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{56}|[a-fA-F0-9]{64}|[a-fA-F0-9]{96}|[a-fA-F0-9]{128}$", "MD6"),
    "RIPEMD160": ("^[a-fA-F0-9]{40}$", "RIPEMD-160"),
    "SHA1": ("^[a-fA-F0-9]{40}$", "SHA-1"),
    "SHA224": ("^[a-fA-F0-9]{56}$", "SHA-224"),
    "SHA256": ("^[a-fA-F0-9]{64}$", "SHA-256"),
    "SHA384": ("^[a-fA-F0-9]{96}$", "SHA-384"),
    # "SHA512": ("^[a-fA-F0-9]{128}$", "SHA-512"),
    "SHA3224": ("^[a-fA-F0-9]{56}$", "SHA3-224"),
    "SHA3256": ("^[a-fA-F0-9]{64}$", "SHA3-256"),
    "SHA3384": ("^[a-fA-F0-9]{96}$", "SHA3-384"),
    # "SHA3512": ("^[a-fA-F0-9]{128}$", "SHA3-512"),
    "SSDEEP": ("^[a-zA-Z0-9/+:.]{1,128}$", "SSDEEP"),
    # "WHIRLPOOL": ("^[a-fA-F0-9]{128}$", "WHIRLPOOL"),
    "TLSH": ("^[a-fA-F0-9]{70}$", "TLSH"),
}

def random_file():
	"""Generates random file
	from word list...
	"""

	return utils.random_word() + utils.random_file_extension().replace("\n", "")

def random_file_hashes():
	"""Generates random
	hash from encoding...
	"""

	encoding = random_encoding()
	return {encoding:random_hash(encoding)}

def random_encoding():
	"""Generates random
	encoding...
	"""

	return list(HASHES_REGEX.keys())[randint(0,len(HASHES_REGEX.keys())) - 1]

def random_hash(encoding):
	"""Generates random
	hash from encoding...
	"""
	
	return rstr.xeger(HASHES_REGEX[encoding][0])

