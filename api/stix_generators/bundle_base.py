"""

STIX2 Bundle Generator

"""

import datetime
import json
import time
import random
import socket
import struct
from stix2 import *
from uuid import uuid4
from .stix_utils import network, websites, files


class BundleBase():
    """
    Bundle base holds all the functions that
    create STIX cyber observable obejcts. The current implementation
    will generate a desired object with random information.
    Current pattern is create_stix_object_name(<variables>)

    Once an object creation function has been created add a key with the
    front end name and refrence to the function as the value.
    The UI will ping an enpoint that calls object_map_json so that users will
    know what obejctsare avilible.
    """

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
        object_array = {
            "IPv4 Address": ["value"],
            "Domain Name": ["value"],
            "MAC Address": ["value"],
            "URL": ["value"],
            "User Account": ["value"],
            "File": ["name", "encoding", "hashes"]
        }
        return json.dumps(object_array)


    def create_bundle(self, objects):
        bundle = Bundle(
            id="bundle--{}".format(uuid4()),
            spec_version="2.0",
            objects=objects
            )

        return bundle


    def create_file_object(self, file_data=None):
        if file_data == None or file_data == {}:
            file_name = files.random_file()
            hashes = files.random_file_hashes()
        else:
            file_name = file_data["name"]
            if "encoding" in file_data.keys():
                encoding = file_data["encoding"]
                hashes = file_data["hashes"]
            else:
                file_name = files.random_file()
                hashes = files.random_file_hashes()
        return File(name=file_name, hashes={encoding:hashes})


    def create_domain_name_object(self, domain_name=None):
        if domain_name == None or domain_name == {}:
            domain_name = website.random_domain()
        else:
            domain_name = domain_name["value"]
        return DomainName(value=domain_name)


    def create_identity_object(self, name):
        id = Identity(name=name, identity_class="events")
        return id


    def create_ipv4_object(self, value=None):
        if value == None or value == {}:
            value = network.random_ipv4()
        else:
            value = value["value"]
        return IPv4Address(value=value)


    def create_mac_address_object(self, mac_address=None):
        if mac_address == None or mac_address == {}:
            mac_address = network.random_mac_address()
        else:
            mac_address = mac_address["value"]
        return MACAddress(value=mac_address)


    def create_url_object(self, value=None):
        if value == None or value == {}:
            value = website.random_url()
        else:
            value = value["value"]

        return URL(value=value)


    def create_user_account_object(self, user_id=None):
        if user_id == None or user_id == {}:
            user_id = uuid4().hex
        else:
            user_id = user_id["value"]

        return UserAccount(user_id=user_id)
