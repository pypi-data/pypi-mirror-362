# Sklik API Python Client
This repository contains unofficial Python client for interacting with the Sklik API. It provides a simple and convenient way for Python applications to generate reports from Seznam Sklik advertising platform.
## Installation
The `sklik` package can be installed from PyPI. You can install it either with pip or with poetry.
### Using pip
Run the following command in your terminal:
```
pip install sklik
```
### Using poetry
Firstly, ensure you have Poetry installed. If it's not installed, refer to the official Poetry installation guide for instructions.
When Poetry is installed, you can add the sklik package to your project by running:
```
poetry add sklik
```
### Using uv
Firstly, ensure you have uv installed. If it's not installed, refer to the official uv installation guide for instructions.
When uv is installed, you can add the sklik package to your project by running:
```
uv add sklik
```
## Classes and Functions Available
The library includes several major Classes and Functions:
`SklikApi`: Class used to instantiate a SklikApi object which is used for making all requests to the Sklik API.
`sklik_request()`: A low-level function to perform a direct POST request to the Sklik API. It can be used separately when lower-level manipulation of requests is required.
`Report`: Class for dealing with large data set from Sklik API by automatically paginating through the data.
`create_report()`: Utility function to create a new report based on several parameters like account, service, date, fields, granularity etc.
## Usage Guide
### Creating Instance of SklikApi
To create Instance of SklikApi, provide your Sklik token:
```python
from sklik import SklikApi

token = '<sklik_token>'
SklikApi.init(token)
```
This sets a default api instance accessible via `SklikApi.get_default_api()`
### Generating A Report
To generate a report, use the create_report function:
```python
from sklik import create_report
from sklik.object import Account

account_id = int('<account_id>')
account = Account(account_id)

report = create_report(
    account, 
    service='campaigns',
    fields=['id', 'name', 'status', 'impressions']
)
```
Please replace `'<account_id>'`, `'service'` and `'fields'` with your specific account details.
### Iterating Through Pages of A Report
To fetch and iterate through the pages of a report, use the Report object returned by `create_report()`:
```python
for page in report:
    print(page)
```
This will print each page of the report in sequence. The Report class is iterable, and it handles pagination automatically.
### Using sklik_request for Low-Level API Access
The `sklik_request` function lets you make API requests directly, giving you low-level access to the API. It requires parameters like api_url, service, method, and args. Note, however, that using this function, you'll need to handle responses on your own.
Example usage:
```python
response = sklik_request(API_URL, "my_service", "my_method", "my_args")
```