APP=$(cat kube/stix_gen_api.yaml |grep "image:" |awk '{print $2}')
UI=$(cat kube/stix_gen_ui.yaml |grep "image:" |awk '{print $2}')
MONGO_HOST="127.0.0.1"
OCP_CLUSTER="127.0.0.1:5000"
ROUTE="http://"
GRAB="/grab_bundle_pretty?id="
URL="http://localhost:5000/"

if docker ps |grep -q "mongo"; then
	echo "MongoDB is running!"
else
	echo "Starting MongoDB"
	docker run -d -p 27017:27017 mongo
fi

if docker ps |grep -q $UI; then
	echo "UI is running!"
else
	echo "Starting UI..."
	docker run -p 8000:3000 -d -e API=$URL $UI
fi

if docker ps |grep -q $APP; then
	echo "API is running!"
else
	echo "Starting API..."
	docker run -p 5000:5000 -d -e MONGO_HOST="127.0.0.1" -e OCP_CLUSTER="127.0.0.1:5000" -e ROUTE="http://" -e GRAB="/grab_bundle_pretty?id=" $APP
fi

echo "All containers running!"