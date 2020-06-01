import requests
import json

def all_Industries():
    r = requests.get('https://api.xforce.ibmcloud.com/industries', headers={ 'Accept': 'application/json',
    'Authorization': 'Basic YzY4YzAzYTEtOTIzZi00OTg4LTgyYTYtNjFiYzFiNmY1Zjc2OmVkYTY3MTZkLTgzMTktNDFjNS1hOTY2LTZhMTgzMzNhMzIzOA=='
    })
    data = json.loads(r.content)
    rows_of_data = data["rows"]
    allIndustries = []

    for objs in rows_of_data:
        curInudstry = objs['name'].replace('Industry Profile', '').strip()

        if curInudstry not in allIndustries:
            allIndustries.append(curInudstry)

    return allIndustries


