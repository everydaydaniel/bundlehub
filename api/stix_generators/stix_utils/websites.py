"""

STIX2 RANDOM UTILS

"""

from random import randint

with open("resources/wordlist.text", "r") as word_file:
	word_list = word_file.readlines()
	word_file.close()


with open("resources/topleveldomains.text", "r") as tld_file:
	tld_list = tld_file.readlines()
	tld_file.close()

RANDOM_ASCII_RANGES = [[48,57], [65, 90], [97,122]]


def random_word():
	"""Generates random
	word of un-specified
	length from word list...
	"""

	length = randint(1, 3)
	word = "-".join([word_list[randint(0, len(word_list))][:-2] for i in range(length)])
	return word[1:]


def random_string():
	"""Generates random string
	of un-specified length...
	"""

	length = randint(1,20)
	word = ""
	for i in range(length):
		ascii_select = randint(0,len(RANDOM_ASCII_RANGES) - 1)
		word += chr(randint(RANDOM_ASCII_RANGES[ascii_select][0], RANDOM_ASCII_RANGES[ascii_select][1]))
	return word


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

	return random_word() + "." + random_top_level_domain()


print(random_string())
