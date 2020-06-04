import datetime
import json
import time
import random
import socket
import struct
from stix2 import *
from uuid import uuid4

class BundleBase():
    """
    docstring for BundleBase.
    Bundle base holds all the functions that
    create STIX cyber observable obejcts. The current implementation
    will generate a desired object with random information.
    Current pattern is create_stix_object_name(<variables>)

    Once an object creation function has been created add a key with the
    front end name and refrence to the function as the value.
    The UI will ping an enpoint that calls object_map_json so that users will
    know what obejctsare avilible.
    """
    # use this object to put all cyber observable
    # creation objects
    def __init__(self, arg):
        self.object_map = {
            "Identity": self.create_identity_object,
            "IPv4 Address": self.create_ipv4_object,
            "Domain Name": self.create_domain_name_object,
            "MAC Address": self.create_mac_address_object,
            "URL": self.create_url_object,
            "User Account": self.create_user_account_object,
            "File": self.create_file_object
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

    def create_file_object(self, file_data=None):
        if file_data == None:
            file_name = "".join(chr(random.randint(97,122)) for i in range(random.randint(1,30))) + ".exe"
            encoding = "MD5"
            hashes = "00000000000000000000000000000000"
        else:
            file_name = file_data["name"]
            if "encoding" in file_data.keys():
                encoding = file_data["encoding"]
                hashes = file_data["hashes"]
            else:
                encoding = "MD5"
                hashes = "00000000000000000000000000000000"
        return File(name=file_name, hashes={encoding:hashes})

    def create_domain_name_object(self, domain_name=None):
        print(domain_name)
        if domain_name == None:
            print("RANDOM")
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

    def create_url_object(self, value=None):
      if value == None:
        tld = [".com",".org",".gov",".edu",".net",".io"]
        proto = "https://"
        base = "".join(chr(random.randint(97,122)) for i in range(random.randint(1,30)))
        base += tld[random.randint(0,len(tld)-1)] + "/"
        ext = uuid4().hex + ".html"
        value = proto + base + ext
      return URL(value=value)

    def create_user_account_object(self, user_id=None):
      if user_id == None:
        id = uuid4().hex
      return UserAccount(user_id=id)
