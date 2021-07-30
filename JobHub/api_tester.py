import requests

API_KEY = "0ce30d04-327c-401b-8ead-9276e407a7b1" # jooble
BASE_URL = "https://jooble.org/api/"
#request headers
headers = {"Content-type": "application/json"}
#json query
body = '{ "keywords": "it", "location": "Bern"}'
response = requests.post(BASE_URL + API_KEY, data=body, headers=headers)
print(response.json()['jobs'][0])

