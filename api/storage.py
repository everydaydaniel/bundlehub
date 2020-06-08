"""

STIX2 Bundle Generator

"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import os

if os.environ["DEV"] == "TRUE":
	MONGO_HOST = "127.0.0.1"
	OCP_CLUSTER = "127.0.0.1:5000"
	ROUTE = ""
else:
	MONGO_HOST = os.environ["MONGO_HOST"]
	OCP_CLUSTER = os.environ["OCP_CLUSTER"]
	ROUTE = "http://stix-gen-route-stix-gen."


##		Prints database and route info 		##
def get_info():
	print("""

	  ██ ██████  ███    ███ 
	  ██ ██   ██ ████  ████ 
	  ██ ██████  ██ ████ ██ 
	  ██ ██   ██ ██  ██  ██ 
	  ██ ██████  ██      ██ 
                      

    STIX-GEN BETA-2.0.1 API CONTAINER

[STIX2 GEN] """ + ROUTE + OCP_CLUSTER + """
[STIX2 GEN] MONGO SERVICE CLUSTER IP AT""" + MONGO_HOST + """\n""")

##		Mongo Connection		##
def mongo_connection():

	client = MongoClient(MONGO_HOST, 27017)
	db = client["stix-gen-db"]
	collection = db["bundles"]
	return client, db, collection


##		Returns bson.ObjectId in string format		##
def store_stix_bundle(bundle, label):

	client, db, collection = mongo_connection()
	bundle["label"] = label
	bundle_row_id = collection.insert_one(bundle).inserted_id
	print(f"[STIX2 GEN] Mongo job finished inserting {bundle_row_id}")
	return ROUTE + OCP_CLUSTER + "/grab_bundle?id=" + str(bundle_row_id)


##		Grabs bundle using string representing bson.ObjectId 		##
def grab_stix_bundle(row_id):

	client, db, collection = mongo_connection()
	result = collection.find_one({"_id": ObjectId(row_id)})
	return result


##		 Bundle search by label 		##
def search(label):

	client, db, collection = mongo_connection()
	results = []
	for stix_obj in collection.find():
		has_key = 'label' in stix_obj.keys()
		if(has_key and stix_obj['label'] == label):
			results.append("http://stix-gen-route-stix-gen." + os.environ["OCP_CLUSTER"] + "/grab_bundle?id=" + str(stix_obj["_id"]))
	print(f"[STIX2 SEARCH] Mongo found {len(results)} stix bundles for {label}")
	return results
