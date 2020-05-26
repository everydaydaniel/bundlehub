import datetime
import json
import time
import random
import socket
import struct
from stix2 import Bundle, IPv4Address, Identity, ObservedData
from uuid import uuid4



def create_bundle(objects):
    bundle = Bundle(
        id="bundle--{}".format(uuid4()),
        spec_version="2.0",
        objects=objects
        )

    return bundle

def create_ipv4_object(value=None):
    if value == None:
        addr = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        return IPv4Address(value=addr)
    return IPv4Address(value=value)


def create_identity(name):
    id = Identity(name=name, identity_class="events")
    return id

def create_observed_data(objects):
    observed_data = ObservedData(
        id="observed-data--{}".format(uuid4()),
        number_observed=1,
        first_observed=datetime.datetime.now(),
        last_observed=datetime.datetime.now(),
        objects={"0": objects}
        )
    return observed_data



def return_bundle():
    addr = create_ipv4_object()
    identity = create_identity(name="db2")
    observed_data = create_observed_data(addr)
    objects = [identity, observed_data]
    bundle = create_bundle(objects)
    return bundle.serialize()
