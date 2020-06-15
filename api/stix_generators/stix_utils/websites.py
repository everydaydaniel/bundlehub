"""

STIX2 RANDOM UTILS

"""

from random import randint
from . import utils

with open("resources/topleveldomains.text", "r") as tld_file:
	tld_list = tld_file.readlines()
	tld_file.close()

HYPERTEXT_PROTOCOLS = ["http://", "https://"]


def random_top_level_domain():
	"""Generates random
	top level domain from
	top level domain list...
	"""

	return tld_list[randint(0, len(tld_list))]


def random_domain():
	"""Builds random
	domain name using
	random top level domains
	and random word generation...
	"""

	return utils.random_word() + "." + random_top_level_domain()


def random_url():
	"""Generates random
	URL using random domain
	and random extensions...
	"""

	protocol = HYPERTEXT_PROTOCOLS[randint(0, len(HYPERTEXT_PROTOCOLS) - 1)]
	domain = random_domain().replace("\n", "")
	ext = utils.random_file_extension().replace("\n", "")
	word = utils.random_word()
	folders = "/".join([utils.random_string() for i in range(randint(1,3))])

	return protocol + domain + "/" + folders + "/" + word + ext




