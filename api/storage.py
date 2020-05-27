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
def store_stix_bundle(bundle, industry):

	client, db, collection = mongo_connection()
	bundle["industry"] = industry
	bundle_row_id = collection.insert_one(bundle).inserted_id
	print("[STIX2 GEN] Mongo job finished inserting ", bundle_row_id)
	return "http://stix-gen-route-stix-gen." + os.environ["OCP_CLUSTER"] + "/grab_bundle?id=" + str(bundle_row_id)


##		Grabs bundle using string representing bson.ObjectId 		##
def grab_stix_bundle(row_id):

	client, db, collection = mongo_connection()
	result = collection.find_one({"_id": ObjectId(row_id)})
	return result


##		 Bundle search by label 		##
def search(industry):

	client, db, collection = mongo_connection()
	results = []
	for stix_obj in collection.find():
		hasKey = 'industry' in stix_obj.keys()
		if(hasKey and stix_obj['industry'] == industry):
			del stix_obj['_id']
			del stix_obj['industry']

			results.append(stix_obj)
	print(f"[STIX2 SEARCH] Mongo found {len(results)} stix bundles for {industry}")
	return results