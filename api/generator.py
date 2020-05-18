"""

STIX2 Bundle Generator

"""

from stix2 import *
import pandas as pd
import json
import datetime


##		Downloads CSV dataset and converts it to a STIX2 bundle		##
def gen_from_url(url):

	df = pd.read_csv(url)
	stamp = datetime.datetime.now()
	stix_objects = []
	stix_observable_objects = []
	stix_object_dict = {
            "type": "observed-data",
            "objects":{},
            "first_observed": stamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "last_observed": stamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "number_observed": 1 }


	##		Create ObservedData		##
	for sdo_index in range(len(df.index)):
		stix_objects.append(IPv4Address(value=df.at[sdo_index, "ip"]))
		stix_objects.append(UserAccount(user_id=df.at[sdo_index, "user"]))
		stix_objects.append(File(name=df.at[sdo_index, "file"], hashes={"SHA-256":df.at[sdo_index, "hashes"]}))
		stix_objects.append(DomainName(value=df.at[sdo_index, "url"]))
		print("[STIX2 GEN] BUILDING SDO ", sdo_index)


		for idx, stix_object in enumerate(stix_objects):
			stix_object_dict["objects"][str(idx)] = json.loads(str(stix_object))
		stix_observable_objects.append(parse(json.dumps(stix_object_dict)))


	##		Generate QRadar Event Bundle		##
	stix_observable_objects.append(Identity(name="QRadar", identity_class="events"))
	bundle = Bundle(stix_observable_objects)

	return bundle