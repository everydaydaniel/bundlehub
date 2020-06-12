"""

STIX2 RANDOM UTILS

"""

from random import randint


OUI_MAP = { "Cisco":"CC:46:D6", "Google": "3C:5A:B4",
			"HP":"3C:D9:2B", 	"Huawei":"00:9A:CD" }


def random_ipv4(HOST_MAX=[192, 168, 1, 254], HOST_MIN=[192, 168, 1, 0]):
	return ".".join(str((randint(HOST_MIN[i], HOST_MAX[i]))) for i in range(4))


def random_mac_address(OUI="Cisco"):
	mac_address = [str(hex(randint(0, 255))[2:]) for i in range(3)]
	for i, bit in enumerate(mac_address):
		if len(bit) == 1:
			mac_address[i] = "0" + bit
	return OUI_MAP[OUI] + ":" + ":".join(mac_address)
