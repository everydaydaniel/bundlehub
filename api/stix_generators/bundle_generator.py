import datetime
import json
import time
import random
import socket
import struct
from .bundle_base import BundleBase
from collections import OrderedDict
from stix2 import Bundle, IPv4Address, Identity, ObservedData
from uuid import uuid4

class BundleGenerate(BundleBase):
    def __init__(self, data=None):
        super().__init__(BundleBase)
        # data schema
        #  {
        #   dataSourceName: "String",
        #   numberOfRows: "Integer",
        #   rowContents: [array, with, selected, objects],
        # }
        self.data = data
        print("data in BundleGenerate:", data)
        self.objects = []
        if data is not None:
            self.parse_data()


    def create_observed_data(self, objects):
        observed_data = ObservedData(
            id="observed-data--{}".format(uuid4()),
            number_observed=len(objects),
            first_observed=datetime.datetime.now(),
            last_observed=datetime.datetime.now(),
            objects=objects
            )
        return observed_data


    def return_bundle(self):
        bundle = self.create_bundle(self.objects)
        return bundle.serialize(pretty=True)



    def create_objects(self, stix_objects, number_of_rows):
        for row in range(number_of_rows):
            object_count = 0
            object_row = OrderedDict()
            for stix_object in stix_objects:
                object_function = self.object_map.get(stix_object)
                if object_function is None:
                    continue
                object_row[str(object_count)] = object_function()
                object_count += 1
            observed_data = self.create_observed_data(object_row)
            self.objects.append(observed_data)

    def check_max_row_num(self, number_of_rows):
        if number_of_rows > 5000:
            number_of_rows = 5000
        return number_of_rows

    def parse_data(self):
        # create the initial identity object and
        # add it into the objects
        name = self.data["dataSourceName"]
        identity = self.create_identity_object(name)
        self.objects.append(identity)
        stix_objects = self.data["rowContents"]
        number_of_rows = self.check_max_row_num(self.data["numberOfRows"])
        self.create_objects(stix_objects, number_of_rows)
