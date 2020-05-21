# STIX2 Bundle Generator

stix-gen is a cloud native API ready to be deployed on OpenShift using Ansible; See `api/README.md` for details on application
routes.

Developers: Andrew Campagna, Charles Neblett, Tyler Stendara, Daniel Herrera

#### Key Features
- Generates dummy QRadar bundles from hosted CSV databases.
- MongoDB storage of all bundles generated.
- Returns back URL that can be used directly with Cloud Pak for Security STIX data connector.

#### How to deploy

1. Ensure you are logged into your OpenShift cluster
2. Clone this repository
3. Edit the `ocp_cluster` variable in `playbook.yaml`

```yaml
---
- hosts: localhost
  roles:
  - deploy.stix.gen

  vars:
    ocp_cluster: YOUR_OCP_CLUSTER_INGRESS_DOMAIN
```

4. Run the ansible script

```bash
ansible-playbook playbook.yaml
```

#### How to use API

1. Locate your stix-gen API route

```bash
oc get routes -n stix-gen |grep stix-gen-route |awk '{print $2}'
```

2. Create a CSV database in the following format

```csv
ip,user,file,hashes,url
```

3. Host it anywhere you would like; GitHub raw user content will work just fine

4. Generate your bundle by utilizing the API route `/gen_from_url` using `url` as an argument

```
http://stix-gen-route-stix-gen.apps.YOUR_OCP_CLUSTER_INGRESS_DOMAIN/gen_from_url?url=URL_TO_RAW_CSV_FILE
```

5. You will be returned back a URL to your STIX Bundle use this directly with the STIX data connector
