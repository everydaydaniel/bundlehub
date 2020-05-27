"""

STIX2 Bundle Generator

"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import generator
import pandas as pd
import storage
import logging


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.debug = True



##		Generates bundle from CSV or JSON database		##
@app.route("/gen_from_url", methods=["GET", "POST"])
def gen_from_url():
	url = request.args.get("url")
	bundle = generator.gen_from_url(url)
	rawbundle = str(bundle["bundle"])
	industry = bundle["industry"]
	jsonbundle = json.loads(rawbundle)
	mongo_bundle_url = storage.store_stix_bundle(jsonbundle, industry)
	return mongo_bundle_url


##		Generates randomly populated bundle 		##
@app.route("/gen_random_bundle", methods=["GET"])
def gen_random_bundle():
	bundle = generator.gen_random_bundle()
	rawbundle = str(bundle["bundle"])
	industry = bundle["industry"]
	jsonbundle = json.loads(rawbundle)
	mongo_bundle_url = storage.store_stix_bundle(jsonbundle, industry)
	return mongo_bundle_url


##		Returns raw bundle by bson.ObjectID 		##
@app.route("/grab_bundle", methods=["GET", "POST"])
def grab_bundle():
	bundle_object_id = request.args.get("id")
	result = storage.grab_stix_bundle(bundle_object_id)
	del result["_id"]
	del result["industry"]
	return json.dumps(result)


##		Returns pretty bundle by bson.ObjectID 		##
@app.route("/grab_bundle_pretty", methods=["GET", "POST"])
def grab_bundle_pretty():
	bundle_object_id = request.args.get("id")
	result = storage.grab_stix_bundle(bundle_object_id)
	del result["_id"]
	del result["industry"]
	return jsonify(result)


##		Search for bundles by label		##
@app.route("/search_bundles", methods=["GET", "POST"])
def search_bundles():
	industry = request.args.get("label")
	result = storage.search(industry)
	return json.dumps(result)
	
if __name__ == "__main__":
	app.run(host="0.0.0.0")
