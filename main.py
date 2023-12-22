import requests


def downloadValue():
    url = 'https://api.nbp.pl/api/exchangerates/rates/A/EUR?format=json'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        value = data['rates'][-1]['mid']
        if value:
            return value
        else:
            return "no exchange rate data"
    except requests.exceptions.RequestException as e:
        return f"Error: No internet connection {e}"


result = downloadValue()
