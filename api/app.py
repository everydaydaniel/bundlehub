"""

STIX2 Bundle Generator

"""

from flask import Flask, jsonify, request
import json
import generator
import pandas as pd
import storage


app = Flask(__name__)
app.debug = True


@app.route("/gen_from_url", methods=["GET", "POST"])
def gen_from_url():
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

@app.route("/gen_random_bundle", methods=["GET"])
def gen_random_bundle():
	rawbundle = generator.randomBundle()
	jsonbundle = json.loads(rawbundle)
	mongo_bundle_url = storage.store_stix_bundle(jsonbundle)
	return mongo_bundle_url

if __name__ == "__main__":
	app.run(host="0.0.0.0")
