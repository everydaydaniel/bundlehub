"""

STIX2 Bundle Generator

"""

from stix2 import *
import pandas as pd
import json
import datetime
import requests


##		Downloads CSV dataset and converts it to a STIX2 bundle		##
def gen_from_csv(url):

    df = pd.read_csv(url)
    stamp = datetime.datetime.now()
    stix_observable_objects = []
    stix_objects = []
    stix_object_dict = {
            "type": "observed-data",
            "objects":{},
            "first_observed": stamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "last_observed": stamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "number_observed": 1 }

    for sdo_index in range(len(df.index)):
        stix_objects.append(IPv4Address(value=df.at[sdo_index, "ip"]))
        stix_objects.append(UserAccount(user_id=df.at[sdo_index, "user"]))
        stix_objects.append(File(name=df.at[sdo_index, "file"], hashes={df.at[sdo_index, "encoding"]:df.at[sdo_index, "hashes"]}))
        stix_objects.append(DomainName(value=df.at[sdo_index, "url"]))
        
        print(f"[STIX2 GEN] BUILDING SDO {sdo_index}")


        for idx, stix_object in enumerate(stix_objects):
            stix_object_dict["objects"][str(idx)] = json.loads(str(stix_object))
        stix_observable_objects.append(parse(json.dumps(stix_object_dict)))
        stix_objects.clear()


    stix_observable_objects.append(Identity(name="QRadar", identity_class="events"))
    bundle = Bundle(stix_observable_objects)

    return bundle


##      Downloads JSON dataset and converts it to a STIX2 bundle     ##
def gen_from_json(url):

    data = json.loads(requests.get(url).content)

    stamp = datetime.datetime.now()
    stix_observable_objects = []
    stix_objects = []
    stix_object_dict = {
            "type": "observed-data",
            "objects":{},
            "first_observed": stamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "last_observed": stamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "number_observed": 1 }

    for sdo_index in range(len(data["objects"])):

        if "MD5" in data["objects"][sdo_index]["file"].keys():
            stix_objects.append(File(name=data["objects"][sdo_index]["file"]["name"], 
                                    hashes={"MD5":data["objects"][sdo_index]["file"]["MD5"]}))
        elif "SHA-1" in data["objects"][sdo_index]["file"].keys():
            stix_objects.append(File(name=data["objects"][sdo_index]["file"]["name"], 
                                    hashes={"SHA-1":data["objects"][sdo_index]["file"]["SHA-1"]}))
        elif "SHA-256" in data["objects"][sdo_index]["file"].keys():
            stix_objects.append(File(name=data["objects"][sdo_index]["file"]["name"], 
                                    hashes={"SHA-256":data["objects"][sdo_index]["file"]["SHA-256"]}))
        else:
            stix_objects.append(File(name=data["objects"][sdo_index]["file"]["name"], 
                                    hashes={"MD5":"00000000000000000000000000000000"}))

        stix_objects.append(IPv4Address(value=data["objects"][sdo_index]["ip"]))
        stix_objects.append(UserAccount(user_id=data["objects"][sdo_index]["user"]))
        stix_objects.append(DomainName(value=data["objects"][sdo_index]["url"]))
        
        print(f"[STIX2 GEN] BUILDING SDO {sdo_index}")


        for idx, stix_object in enumerate(stix_objects):
            stix_object_dict["objects"][str(idx)] = json.loads(str(stix_object))
        stix_observable_objects.append(parse(json.dumps(stix_object_dict)))
        stix_objects.clear()


    stix_observable_objects.append(Identity(name="QRadar", identity_class="events"))
    bundle = Bundle(stix_observable_objects)

    return bundle