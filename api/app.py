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
from stix_generators.bundle_generator import BundleGenerate



app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.debug = True

@app.route("/")
def homepage():
	return "hello"

@app.route("/gen_from_url", methods=["GET", "POST"])
def gen_from_url():
	# industry = request.args.get("industry") upon setting a custom sitx bundle, ask for label as well to search for
	url = request.args.get("url")
	rawbundle = str(generator.gen_from_url(url))
	jsonbundle = json.loads(rawbundle)
	mongo_bundle_url = storage.store_stix_bundle(jsonbundle)
	return mongo_bundle_url


@app.route("/grab_bundle", methods=["GET", "POST"])
def grab_bundle():
	bundle_object_id = request.args.get("id")
	result = storage.grab_stix_bundle(bundle_object_id)
	del result["_id"]
	return json.dumps(result)

@app.route("/create_bundle", methods=["GET","POST"])
def create_bundle():
	data = request.get_json()
	bundle_gen = BundleGenerate(data)
	bundle = bundle_gen.return_bundle()
	return bundle

@app.route("/gen_random_bundle", methods=["GET"])
def gen_random_bundle():
	rawbundle = generator.randomBundle()
	jsonbundle = json.loads(rawbundle)
	# jsonbundle["industry"] = "healthcare"
	mongo_bundle_url = storage.store_stix_bundle(jsonbundle)
	return mongo_bundle_url


@app.route("/search_bundles", methods=["GET", "POST"])
def search_bundles():
	bundle_label = request.args.get("label")
	result = 'GRAB STIX BUNDLE THAT WAS SEARCHED'
	# if none are returned try fuzzy search
	monogo_bundle_url = 'GET URLS FROM MONDODB'

if __name__ == "__main__":
	app.run(host="0.0.0.0")
