if docker ps |grep -q "mongo"; then
	echo "MongoDB is running!"
else
	echo "Starting MongoDB"
	docker run -d -p 27017:27017 mongo
fi

export MONGO_HOST="127.0.0.1"
export OCP_CLUSTER="127.0.0.1:5000"
export ROUTE="http://"
export GRAB="/grab_bundle_pretty?id="
export API="http://localhost:5000/"

python3 api/app.py