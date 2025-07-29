# postcodewizard-python-client


---

## Usage

The official API documentation [PostcodeWizard API](https://api.postcodewizard.nl/docs/api).

```
from postcodewizard.client import PostcodeWizard

client = PostcodeWizard("API_KEY_HERE")

# Lookup
result = client.lookup("7223LN", "1")

# Autocomplete
result =  client.autocomplete("Toverstraat 1, Baak")
```
