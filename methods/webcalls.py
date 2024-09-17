import requests

def Get(url, headers):
    return requests.get(url, headers=headers, timeout=None, stream=True)