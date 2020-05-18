oc delete -f kube/mongo.yaml
oc delete -f kube/mongo_config.yaml
oc delete -f kube/mongo_svc.yaml
oc delete -f kube/stix_gen_api.yaml
oc delete -f kube/stix_gen_route.yaml
oc delete -f kube/stix_gen_svc.yaml
oc delete project stix-gen