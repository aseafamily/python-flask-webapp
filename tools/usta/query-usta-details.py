import requests
import json

# Define the URL and headers
url = 'https://www.usta.com/usta/api?type=playerInfo'
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'csrf-token': 'undefined',
    'origin': 'https://www.usta.com',
    'priority': 'u=1, i',
    'referer': 'https://www.usta.com/en/home/play/player-search/profile.html',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
}

# Define the data payload
payload = {
    "selection": {
        "uaid": "2018248404"
    },
    "output": {
        "ratings": "true",
        "extendedProfile": "true",
        "wtn": "true"
    }
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print the response
if response.status_code == 200:
    print("Response JSON:\n", json.dumps(response.json(), indent=2))
else:
    print(f"Request failed with status code {response.status_code}")
