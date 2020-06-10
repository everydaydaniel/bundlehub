"""

STIX2 Bundle Generator

"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import storage
import logging
import os
from bundlehub import bundlehub
from stix_generators.bundle_generator import BundleGenerate
from stix_generators.bundle_base import BundleBase
from stix_generators.bundle_validate import BundleValidate
from stix_generators.get_Industries import all_Industries

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.debug = True

print("""

	  ██ ██████  ███    ███ 
	  ██ ██   ██ ████  ████ 
	  ██ ██████  ██ ████ ██ 
	  ██ ██   ██ ██  ██  ██ 
	  ██ ██████  ██      ██ 
                      

    STIX-GEN BETA-2.1.0 API CONTAINER""")

print(storage.get_info())


##		Tag and transform bundle for storage		##
def transform_bundle(bundle):
	rawbundle = str(bundle)
	jsonbundle = json.loads(rawbundle)
	return jsonbundle


##		Used with UI to get the availible object maps 		##
@app.route("/get_object_map", methods=["GET","POST"])
def get_object_map():
	bundle_object = BundleGenerate()
	print(bundle_object.object_map_json())
	return bundle_object.object_map_json()


##		Used with UI to pass in data and create a bundle 		##
@app.route("/create_bundle", methods=["GET","POST"])
def create_bundle():
	data = request.get_json()
	data = data["input"]
	bundle_gen = BundleGenerate(data)
	bundle = bundle_gen.return_bundle()
	mongo_bundle_url = storage.store_stix_bundle(transform_bundle(bundle), label=data["label"])

	response = {
		"url": mongo_bundle_url,
		"bundle_data": bundle.serialize(),
	}

	return json.dumps(response)


##		Validate custom bundle bundle 		##
@app.route("/validate", methods=["GET", "POST"])
def validate():
	data = request.get_json()
	data = data["input"]
	bundle_validation = BundleValidate(data)
	response = bundle_validation.get_response()
	return json.dumps(response)


##		Returns raw bundle by bson.ObjectID 		##
@app.route("/grab_bundle", methods=["GET", "POST"])
def grab_bundle():
	bundle_object_id = request.args.get("id")
	result = storage.grab_stix_bundle(bundle_object_id)
	del result["_id"]
	del result["label"]
	return json.dumps(result)


##		Returns pretty bundle by bson.ObjectID 		##
@app.route("/grab_bundle_pretty", methods=["GET", "POST"])
def grab_bundle_pretty():
	bundle_object_id = request.args.get("id")
	result = storage.grab_stix_bundle(bundle_object_id)
	del result["_id"]
	del result["label"]
	return jsonify(result)


##		Search for bundles by label		##
@app.route("/search_bundles", methods=["GET", "POST"])
def search_bundles():
	label = request.args.get("label")
	results = storage.search(label)
	return jsonify(dict(search_results=results))


##		Get all industries	##
@app.route("/allIndustries", methods=["GET"])
def allindustries():
	result = all_Industries()
	return json.dumps(result)

if __name__ == "__main__":
	app.run(host="0.0.0.0")
