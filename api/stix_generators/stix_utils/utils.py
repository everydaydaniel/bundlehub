"""

STIX2 RANDOM UTILS

"""

from random import randint
import os

wd = os.popen("pwd").read().replace("\n", "")

with open(wd + "/resources/wordlist.text", "r") as word_file:
	word_list = word_file.readlines()
	word_file.close()

with open(wd + "/resources/fileextensions.text", "r") as ext_file:
	ext_list = ext_file.readlines()
	ext_file.close()

RANDOM_ASCII_RANGES = [[48,57], [65, 90], [97,122]]

def sift_dictionary(data):
	"""Clears out empty
	strings from input JSON...
	"""

	return_dict = {}
	for key, value in data.items():
		if type(value) is dict:
			return_dict[key] = sift_dictionary(value)
		else:
			if value == "":
				continue
			return_dict[key] = value
	return return_dict

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

def random_file_extension():
	"""Generates random
	file extension from
	file extension list...
	"""

	return ext_list[randint(0, len(ext_list) - 1)]






