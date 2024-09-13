import requests

result = requests.post('http://127.0.0.1:8000/api/save_entries/',
    json=[{"title": "Cars", "entries": [{"title": "21214"}]}])


print(result)