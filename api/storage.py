"""

STIX2 Bundle Generator

"""

from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import os


MONGO_HOST = os.environ["MONGO_HOST"]
OCP_CLUSTER = os.environ["OCP_CLUSTER"]
ROUTE = os.environ["ROUTE"]
GRAB = os.environ["GRAB"]


##		Prints database and route info 		##
def get_info():

	return ("""
[STIX2 GEN] """ + ROUTE + OCP_CLUSTER + """
[STIX2 GEN] MONGO SERVICE CLUSTER IP AT """ + MONGO_HOST + """\n""")

##		Mongo Connection		##
def mongo_connection():

	client = MongoClient(MONGO_HOST, 27017)
	db = client["stix-gen-db"]
	collection = db["bundles"]
	return client, db, collection


##		Returns bson.ObjectId in string format		##
def store_stix_bundle(bundle, label, industry, dataSourceName, template):

	def creatingTemplate(returning_template, storing_template):
		if returning_template:
			previewObjects = returning_template['objects'][0:2]
			returning_template['objects'] = previewObjects
			del returning_template['_id']
			del returning_template['label']
			del returning_template['industry']
			del returning_template['dataSourceName']
			bundle_template = json.dumps(returning_template)
			return bundle_template
			
		elif storing_template:
			
			template = {}
			previewObjects = storing_template['objects'][0:2]
			template['id'] = storing_template['id']
			template['spec_version'] = storing_template['spec_version']
			template['objects'] = previewObjects

			storing_template['template'] = template
			return storing_template

	client, db, collection = mongo_connection()
	bundle["label"] = label
	bundle["industry"] = industry
	bundle["dataSourceName"] = dataSourceName
	bundle["template"] = template
	returning_bundle = bundle

	if template:
		returning_bundle = creatingTemplate(False, bundle)

	bundle_row_id = collection.insert_one(returning_bundle).inserted_id
	print(f"[STIX2 GEN] Mongo job finished inserting {bundle_row_id}")

	if template:
		bundle_template = creatingTemplate(bundle, False)

		return {'bundle_url': ROUTE + "." + OCP_CLUSTER + GRAB + str(bundle_row_id), 'template': bundle_template}
	elif template == False:
		return {'bundle_url': ROUTE + "." + OCP_CLUSTER + GRAB + str(bundle_row_id), 'template': False}



##		Grabs bundle using string representing bson.ObjectId 		##
def grab_stix_bundle(row_id):

	client, db, collection = mongo_connection()
	result = collection.find_one({"_id": ObjectId(row_id)})
	# print('RESULT', result)
	return result


##		 Bundle search by label 		##
def search(label):

	client, db, collection = mongo_connection()
	results = []
	for stix_obj in collection.find():
		has_key = 'label' in stix_obj.keys()
		if(has_key and stix_obj['label'] == label):

			results.append({"bundleUrl": "http://stix-gen-route-stix-gen." + os.environ["OCP_CLUSTER"] + "/grab_bundle?id=" + str(stix_obj["_id"]),
			"industry": stix_obj["industry"], 'dataSourceName': stix_obj["dataSourceName"]
			})
	print(f"[STIX2 SEARCH] Mongo found {len(results)} stix bundles for {label}")
	return results
