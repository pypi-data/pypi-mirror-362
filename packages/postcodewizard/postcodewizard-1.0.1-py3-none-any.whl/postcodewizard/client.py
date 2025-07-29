import http.client
import urllib.parse
from urllib.parse import urlparse
import json

POSTCODE_WIZARD_API_URL = "https://api.postcodewizard.nl"

class PostcodeWizard:
    def __init__(self, api_key: str, base_url: str = POSTCODE_WIZARD_API_URL):
        self._api_key = api_key
        self._headers = {
            "x-api-key": self._api_key,
            "Accept": "application/json"
        }
        self._base_url = base_url
        parsed = urlparse(base_url)
        self._conn = http.client.HTTPSConnection(parsed.hostname)

    def lookup(self, postal_code: str, house_number: str) -> str:
        endpoint = f"/lookup?postcode={postal_code}&houseNumber={house_number}"
        return self._request(endpoint)

    def autocomplete(self, query: str) -> str:
        encoded_query = urllib.parse.quote(query)
        endpoint = f"/autocomplete?query={encoded_query}"
        return self._request(endpoint)

    def _request(self, endpoint: str):
        self._conn.request("GET", endpoint, headers=self._headers)
        response = self._conn.getresponse()
        result = response.read().decode("utf-8")

        if response.status != 200:
            raise Exception(f"API Error {response.status}: {result}")

        return json.loads(result)
