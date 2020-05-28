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

class BundleBase():
    """docstring for BundleBase."""
    # use this object to put all cyber observable
    # creation objects
    def __init__(self, arg):
        self.object_map = {
            "Identity": self.create_identity_object,
            "IPv4Address": self.create_ipv4_object
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

    def create_identity_object(self, name):
        id = Identity(name=name, identity_class="events")
        return id

    def create_ipv4_object(self, value=None):
        if value == None:
            addr = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
            return IPv4Address(value=addr)
        return IPv4Address(value=value)

    def create_observed_data(self, objects):
        observed_data = ObservedData(
            id="observed-data--{}".format(uuid4()),
            number_observed=1,
            first_observed=datetime.datetime.now(),
            last_observed=datetime.datetime.now(),
            objects={"0": objects}
            )
        return observed_data
