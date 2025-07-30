# teamdbapi
This module enables you to easily access the TeamDB Web API.

- Package version: 3.8.0
- TeamDB Web API version: 2.0

## Requirements.

- Python 3.4+
- TeamDB 3.8.0

## <a name="install">Installation and usage</a>
### pip install

Install via  [pip](http://pypi.python.org/pypi/pip).

```sh
pip install teamdbapi
```

Then import the package:
```python
import teamdbapi 
```

## Getting Started

Please follow the [installation procedure](#install) and then run the following:

```python
import teamdbapi
from teamdbapi.rest import ApiException

# Create a Configuration object
configuration = teamdbapi.Configuration()
configuration.host = "http://localhost:9001" # Replace with your TeamDB API address if different

# Create an instance of the Client API
client_api = teamdbapi.ApiClient(configuration)

# Create an instance of the Assembly API using the client_api
assembly_api = teamdbapi.AssemblyApi(client_api)

# Try to execute the request
try:

    # Get response with http info (Content, HTTP Status Code, HTTP Header)
    result = assembly_api.select_current_assembly_with_http_info(assembly_id = "6189993b-ad4d-4c41-8268-8419a63e5554")
    print(result)

    # Get only response content
    result = assembly_api.select_current_assembly(assembly_id = "6189993b-ad4d-4c41-8268-8419a63e5554")
    print(result)

except ApiException as e:
    print("Exception when selecting the current assembly : %s\n" % e)
```

## Documentation for API Endpoints

With a TeamDB Client, check the documentation at *http://localhost:9001* (Default value for the TeamDB Web API URL)

## Documentation For Authorization

Endpoints are subject to the same authorization as in TeamDB.

## Author

Trackside Software
support@trackside.fr

