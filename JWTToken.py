
import jwt
import time
import requests
import json
import os
key_file='key_file.key'

from dotenv import load_dotenv
load_dotenv()
  
myurl= os.getenv('url')
issuer = os.getenv('iss')
user = os.getenv('user')

with open(key_file) as fd:
  private_key = fd.read()

payload = {
      'iss': issuer,
      'exp': int(time.time()) + 300,
      'aud': myurl,
      'sub': user
    }
    
encoded = jwt.encode(payload, private_key, algorithm='RS256')
print('JWT:', encoded )

r = requests.post(myurl + '/services/oauth2/token', data = {
    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    'assertion': encoded,
  })

print('Status:', r.status_code)
access_token = r.json().get("access_token")
instance_url = r.json().get("instance_url")
print("Access Token:", access_token)
print("Instance URL", instance_url)


def sf_api_call(action, parameters = {}, method = 'get', data = {}):
    
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }
    if method == 'get':
        r = requests.request(method, instance_url+action, headers=headers, params=parameters, timeout=30)
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
    else:
        # error for methods not implemented in this code
        raise ValueError('Method should be get or post or patch.')
    print('Debug: API %s call: %s' % (method, r.url) )
    if r.status_code < 300:
        if method=='patch':
            return None
        else:
            return r.json()
    else:
        raise Exception('API error when calling %s : %s' % (r.url, r.content))

print(json.dumps(sf_api_call('/services/data/v39.0/query/', {
    'q': 'SELECT Account.Name, Name, CloseDate from Opportunity where IsClosed = False order by CloseDate ASC LIMIT 10'
  }), indent=2))