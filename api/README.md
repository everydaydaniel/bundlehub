# STIX2 Bundle Generator API

#### Routes

```python
@app.route("/gen_from_url", methods=["GET", "POST"])
```
  - args: [url]
  - description: Downloads CSV database from URL and converts to STIX2 Bundle Raw Text
  - returns url for data source connection to Cloud Pak for Security
  
```python
@app.route("/gen_random_bundle", methods=["GET", "POST"])
```
  - args: None
  - description: Creates a random bundle filled with junk data
  - returns url for data source connection to Cloud Pak for Security
  
  
```python
@app.route("/grab_bundle", methods=["GET", "POST"])
```
- args: [id]
- description: Finds STIX2 bundle in MongoDB using bson.ObjectId
- returns raw bundle string

```python
@app.route("/grab_bundle_pretty", methods=["GET", "POST"])
```
- args: [id]
- description: Finds STIX2 bundle in MongoDB using bson.ObjectId
- returns prettified bundle string

```python
@app.route("/search_bundles", methods=["GET", "POST"])
```
- args: [label]
- description: Finds all bundles with matching label
- returns list of bundle ID's

