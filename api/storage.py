"""

STIX2 Bundle Generator

"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import os


##		Mongo Connection		##
def mongo_connection():

	client = MongoClient(os.environ["MONGO_HOST"], 27017)
	db = client["stix-gen-db"]
	collection = db["bundles"]
	return client, db, collection


##		Returns bson.ObjectId in string format		##
def store_stix_bundle(bundle, label):

	client, db, collection = mongo_connection()
	bundle["label"] = label
	bundle_row_id = collection.insert_one(bundle).inserted_id
	print(f"[STIX2 GEN] Mongo job finished inserting {bundle_row_id}")
	return "http://stix-gen-route-stix-gen." + os.environ["OCP_CLUSTER"] + "/grab_bundle?id=" + str(bundle_row_id)


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
