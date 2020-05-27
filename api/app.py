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


@app.route("/gen_from_url", methods=["GET", "POST"])
def gen_from_url():
	url = request.args.get("url")
	obj = generator.gen_from_url(url)
	rawbundle = str(obj["bundle"])
	industry = obj["industry"]
	jsonbundle = json.loads(rawbundle)
	mongo_bundle_url = storage.store_stix_bundle(jsonbundle, industry)
	return mongo_bundle_url


@app.route("/grab_bundle", methods=["GET", "POST"])
def grab_bundle():
	bundle_object_id = request.args.get("id")
	result = storage.grab_stix_bundle(bundle_object_id)
	del result["_id"]
	# del result["industry"]
	return json.dumps(result)


@app.route("/gen_random_bundle", methods=["GET"])
def gen_random_bundle():
	obj = generator.gen_random_bundle()
	rawbundle = str(obj["bundle"])
	industry = obj["industry"]
	jsonbundle = json.loads(rawbundle)
	mongo_bundle_url = storage.store_stix_bundle(jsonbundle, industry)
	return mongo_bundle_url


@app.route("/search_bundles", methods=["GET", "POST"])
def search_bundles():
	industry = request.args.get("label")
	result = storage.search(industry)
	return json.dumps(result)
	
if __name__ == "__main__":
	app.run(host="0.0.0.0")
