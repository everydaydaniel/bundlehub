"""

STIX2 Bundle Generator

"""

from stix2 import *
import pandas as pd
import json
import datetime
from stix_generators import randomsdo

##      Generates random bundle of SDO's        ##
def gen_random_bundle():
    
    md5 = randomsdo.hashing()
    new_observables = randomsdo.creatingObservedObject()
    industry = randomsdo.randomIndustry()

    indicator = Indicator(
    name="File hash for malware variant",
    labels=["malicious-activity"], 
    pattern=f"[file:hashes.md5 = '{md5}']")

    observed = ObservedData(
    first_observed='2019-10-10T10:41:43.0469296Z', 
    last_observed=indicator["valid_from"], 
    number_observed=len(new_observables), 
    objects=new_observables)

    malware = Malware(
    name="CryptoLocker", 
    id="malware--81be4588-96a8-4de2-9938-9e16130ce7e6",
    description="CryptoLocker is known to be malicious ransomware.",
    labels=['remote-access-trojan'])

    relationship = Relationship(
    relationship_type='indicates',
    source_ref=indicator.id,
    target_ref=indicator.id)

    bundle = Bundle(indicator, observed, malware)
    return {"bundle": bundle, "industry": industry}
