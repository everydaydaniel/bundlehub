"""

STIX2 Bundle Generator

"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import pandas as pd
import storage
import logging
import stix_generators.bundle_from_random as randombundle
import stix_generators.bundle_from_file as generator
from stix_generators.bundle_generator import BundleGenerate
from stix_generators.bundle_base import BundleBase
from stix_generators import randomsdo
from stix_generators.get_Industries import all_Industries

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.debug = True


@app.route("/")
def homepage():
	return "hello"


##		Tag and transform bundle for storage		##
def transform_bundle(bundle):
	rawbundle = str(bundle)
	jsonbundle = json.loads(rawbundle)
	return jsonbundle


##		Used with UI to get the availible object maps 		##
@app.route("/get_object_map", methods=["GET","POST"])
def get_object_map():
	bundle_object = BundleGenerate()
	return bundle_object.object_map_json()


##		Used with UI to pass in data and create a bundle 		##
@app.route("/create_bundle", methods=["GET","POST"])
def create_bundle():
	# expected input
	# data = {
	#         "dataSourceName": "testBundle",
	#         "numberOfRows": 10,
	#         "rowContents": ["IPv4Address"]
	#         }
	data = request.get_json()
	data = data["input"]
	bundle_gen = BundleGenerate(data)
	bundle = bundle_gen.return_bundle()
	return bundle


##		Generates bundle from CSV or JSON database		##
@app.route("/gen_from_url", methods=["GET", "POST"])
def gen_from_url():
	url = request.args.get("url")
	label = request.args.get("label")

	if url.split(".")[-1] == "csv":
		bundle = generator.gen_from_csv(url)
	elif url.split(".")[-1] == "json":
		bundle = generator.gen_from_json(url)
	else:
		return "INVALID URL"

	mongo_bundle_url = storage.store_stix_bundle(transform_bundle(bundle), label)
	return mongo_bundle_url


##		Generates randomly populated bundle 		##
@app.route("/gen_random_bundle", methods=["GET"])
def gen_random_bundle(): # need to add implementation into cyber objects for entered and random industries
	label = request.args.get("label") or randomsdo.randomIndustry() 
	bundle = randombundle.gen_random_bundle()
	mongo_bundle_url = storage.store_stix_bundle(bundle, label)
	return mongo_bundle_url


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
	result = storage.search(label)
	return json.dumps(result)

##		Get all industries	##
@app.route("/allIndustries", methods=["GET"])
def allindustries():
	result = all_Industries()
	return json.dumps(result)

if __name__ == "__main__":
	app.run(host="0.0.0.0")
