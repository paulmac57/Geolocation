import requests

url = "https://alexnormand-dino-ipsum.p.rapidapi.com/"

querystring = {"format":"csv","words":"30","paragraphs":"30"}

headers = {
    'x-rapidapi-host': "alexnormand-dino-ipsum.p.rapidapi.com",
    'x-rapidapi-key': "sfdNZa0o9cmsh1Ti3vTo51syMF2Zp192iAwjsnCWY5vhsHodXE"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
'''

OR 

import requests

params = {"words": 10, "paragraphs": 1, "format": "json"}

response = requests.get(f"https://alexnormand-dino-ipsum.p.rapidapi.com/", params=params,
 headers={
   "X-RapidAPI-Host": "alexnormand-dino-ipsum.p.rapidapi.com",
   "X-RapidAPI-Key": "4xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
 }
)

print (type(response.json()))
print(response.json()) '''