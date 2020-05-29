import datetime
import json
import time
import random
import socket
import struct
from stix2 import *
from uuid import uuid4

class BundleBase():
    """docstring for BundleBase."""
    # use this object to put all cyber observable
    # creation objects
    def __init__(self, arg):
        self.object_map = {
            "Identity": self.create_identity_object,
            "IPv4 Address": self.create_ipv4_object,
            "Domain Name": self.create_domain_name_object,
            "MAC Address": self.create_mac_address_object
        }

    def object_map_json(self):
        object_array = [key for key in self.object_map if key is not "Identity"]
        return json.dumps(object_array)

    def create_bundle(self, objects):
        bundle = Bundle(
            id="bundle--{}".format(uuid4()),
            spec_version="2.0",
            objects=objects
            )

        return bundle

    def create_domain_name_object(self, domain_name=None):
        if domain_name == None:
            tld = [".com",".org",".gov",".edu",".net",".io"]
            domain_name = "".join(chr(random.randint(97,122)) for i in range(random.randint(1,30)))
            domain_name += tld[random.randint(0,len(tld)-1)]
        return DomainName(value=domain_name)

    def create_identity_object(self, name):
        id = Identity(name=name, identity_class="events")
        return id

    def create_ipv4_object(self, value=None):
        if value == None:
            addr = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
            return IPv4Address(value=addr)
        return IPv4Address(value=value)

    def create_mac_address_object(self, mac_address=None):
        if mac_address == None:
            mac = [ 0x00, 0x16, 0x3e,
                random.randint(0x00, 0x7f),
                random.randint(0x00, 0xff),
                random.randint(0x00, 0xff) ]
            mac_address = ':'.join(map(lambda x: "%02x" % x, mac))
        return MACAddress(value=mac_address)
