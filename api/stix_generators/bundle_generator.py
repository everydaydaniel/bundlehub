"""

STIX2 Bundle Generator

"""

import datetime
import json
import time
import random
import socket
import struct
from .bundle_base import BundleBase
from collections import OrderedDict
from stix2 import Bundle, IPv4Address, Identity, ObservedData
from .stix_utils.utils import sift_dictionary
from uuid import uuid4


class BundleGenerate(BundleBase):
    """
    BundleGenerate manages complete generation
    of random and custom bundle content...
    """

    def __init__(self, data=None):
        super().__init__(BundleBase)
        self.data = data
        print("data in BundleGenerate:", data)
        self.objects = []
        if data is not None:
            self.custom_data = self.parse_custom()
            self.parse_data()


    def create_observed_data(self, objects):
        observed_data = ObservedData(
            id="observed-data--{}".format(uuid4()),
            number_observed=1,
            first_observed=datetime.datetime.now(),
            last_observed=datetime.datetime.now(),
            objects=objects
            )
        return observed_data


    def return_bundle(self):
        bundle = self.create_bundle(self.objects)
        print(f"[STIX2 GEN] BUILD BUNDLE COMPLETE ")
        return bundle


    def create_objects(self, stix_objects, number_of_rows):
        for row in range(number_of_rows):
            sdo_dict = {}
            for sdo_idx, stix_object in enumerate(stix_objects):
                object_function = self.object_map.get(stix_object)
                if object_function is None:
                    continue
                if row in self.custom_data.keys():
                    if stix_object in self.custom_data[row].keys():
                        sdo_dict[str(sdo_idx)] = object_function(self.custom_data[row][stix_object])
                else:
                    sdo_dict[str(sdo_idx)] = object_function()
            observed_data = self.create_observed_data(sdo_dict)
            self.objects.append(observed_data)


    def check_max_row_num(self, number_of_rows):
        if number_of_rows > 5000:
            number_of_rows = 5000
        return number_of_rows


    def parse_custom(self):
        customized = {}
        if len(self.data["custom"]) == 0:
            return customized
        self.data["custom"] = [sift_dictionary(obj) for obj in self.data["custom"]]
        print(self.data["custom"])
        for custom_observed in self.data["custom"]:
            random_index = None
            while(True):
                random_index = random.randint(0,self.data["numberOfRows"] - 1)
                if random_index not in customized.keys():
                    break

            customized[random_index] = custom_observed
        return customized


    def parse_data(self):
        name = self.data["dataSourceName"]
        identity = self.create_identity_object(name)
        self.objects.append(identity)
        stix_objects = self.data["rowContents"]
        number_of_rows = self.check_max_row_num(self.data["numberOfRows"])
        self.create_objects(stix_objects, number_of_rows)
