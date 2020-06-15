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
from .stix_utils import network, websites, files, utils


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
        """Provides front-end JS
        a dictionary for custom
        values input...
        """

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
        """Packages all SDO into a bundle...
        """

        bundle = Bundle(
            id="bundle--{}".format(uuid4()),
            spec_version="2.0",
            objects=objects
        )

        return bundle


    def create_file_object(self, file_data=None):
        """Generates a new File SDO
        either with custom data or
        from random utils...
        """

        if file_data == None or file_data == {}:
            file_name = files.random_file()
            hash_data = files.random_file_hashes()
        else:
            file_name = file_data.get("name")

            if "encoding" in file_data.keys():
                hash_data = {file_data["encoding"]:file_data["hashes"]}
            else:
                hash_data = files.random_file_hashes()

        return File(name=file_name, hashes=hash_data)


    def create_domain_name_object(self, domain_name=None):
        """Generates a new Domain Name SDO
        either with custom data or
        from random utils...
        """

        if domain_name == None or domain_name == {}:
            domain_name = websites.random_domain()
        else:
            domain_name = domain_name["value"]

        return DomainName(value=domain_name)


    def create_identity_object(self, name):
        """Creates identity for
        connector validation...
        """

        id = Identity(name=name, identity_class="events")
        return id


    def create_ipv4_object(self, value=None):
        """Generates a new IPv4 Address
        SDO either with custom data or
        from random utils...
        """

        if value == None or value == {}:
            value = network.random_ipv4()
        else:
            value = value["value"]

        return IPv4Address(value=value)


    def create_mac_address_object(self, mac_address=None):
        """Generates a new MAC Address
        SDO either with custom data or
        from random utils...
        """

        if mac_address == None or mac_address == {}:
            mac_address = network.random_mac_address()
        else:
            mac_address = mac_address["value"]

        return MACAddress(value=mac_address)


    def create_url_object(self, value=None):
        """Generates a new URL SDO
        either with custom data or
        from random utils...
        """

        if value == None or value == {}:
            value = websites.random_url()
        else:
            value = value["value"]

        return URL(value=value)

    def create_user_account_object(self, user_id=None):
        """Generates a new User Account
        SDO either with custom data or
        from random utils...
        """

        if user_id == None or user_id == {}:
            user_id = utils.random_word()
        else:
            user_id = user_id["value"]

        return UserAccount(user_id=user_id)
