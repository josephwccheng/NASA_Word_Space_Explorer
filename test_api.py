import requests

base_url = "http://127.0.0.1:5000"

response = requests.get(base_url + "/documentMetadata/19970027742")
print(response.json())

payload = {"documentList": ['19700021346', '20040173138', '19980038066', '19980237279', '20040121602']}
response = requests.post(base_url + "/documentMultipleMetadata", json=payload)
print(response.json())


payload = {"query": "this is testing for nasa hackathon 2022"}
response = requests.post(base_url + "/searchEngine", json=payload)
print(response.json())


payload = {"query": "this is testing for nasa hackathon 2022"}
response = requests.post(base_url + "/tagRecommender", json=payload)
print(response.json())