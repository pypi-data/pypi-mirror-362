import os
import sys
import pytest

from postcodewizard.client import PostcodeWizard

@pytest.fixture
def client():
    return PostcodeWizard("API_KEY_HERE")

def test_lookup(client):
    result = client.lookup("7223LN", "1")
    expected = {
        "postcode": "7223LN",
        "number": "1",
        "letter": None,
        "addition": None,
        "full_number": "1",
        "street": "Toverstraat",
        "city": "Baak",
        "coordinates": {
            "longitude": "52.0828616",
            "latitude": "6.2524736"
        }
    }

    assert result == expected

def test_autocomplete(client):
    results = client.autocomplete("Toverstraat 1, Baak")
    assert isinstance(results, list)
    assert any(item["postcode"] == "7223LN" and item["number"] == "1" for item in results)
