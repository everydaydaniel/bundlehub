import hashlib 
import random
import string
import stix2 

ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

def constructRandomString(num):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(num))

def hashing():
    str_result = constructRandomString(random.randint(0 ,10))
    result = hashlib.md5(str_result.encode()) 
    return result.hexdigest()

def urlGen():
    domain = constructRandomString(random.randint(4, 9))
    url = "www." + domain + ".com"
    return url

def randomNum(maxLength):
    return random.randint(1, maxLength)

def randomEmail():
    acc = constructRandomString(random.randint(2, 7))
    email = f"{acc}@example.com"
    fullName = acc + " " + "last_name"
    return {'email': email, 'fullName': fullName}

def creatingObservedObject():
    results = {}
    randomAcc = randomEmail()
    idy = stix2.Identity(name='John Doe', identity_class="individual")
    types = {"ipv4-addr": stix2.IPv4Address(value=ip, _valid_refs={"1": "mac-addr", "2": "mac-addr"}), 
    "user-account": stix2.UserAccount(user_id=randomNum(1000)), "File": stix2.File(name=idy["name"], size=random.randint(1000000, 25000000)), 
    "Domain":  stix2.v20.observables.URL(value=urlGen()), 
    "email-addr": stix2.EmailAddress(value=randomAcc['email'], display_name=randomAcc['fullName'])}    
    rand = randomNum(len(types) + 1) 

    count = 0
    for key in types.keys():
        if count == rand:
            break
        results[f"{count}"] = types[key]
        count += 1
    return results
