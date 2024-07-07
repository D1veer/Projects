import requests
import json

# category = input().lower()
api_url = 'https://api.quotable.io/quotes/random?tags=technology,famous-quotes'
response = requests.get(api_url)
if response.status_code == requests.codes.ok:
  print(response.text)
  res = json.loads(response.text)
  print(res["content"])
  print(res["author"])
  print(res["tags"])
else:
  print("Error:", response.status_code, response.text)