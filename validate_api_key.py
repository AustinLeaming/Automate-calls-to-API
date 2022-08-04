"""
Validate API key returns "OK" response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.authentication_api import AuthenticationApi

resposne = ""

def make_call():
    global response
    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = AuthenticationApi(api_client)
        response = api_instance.validate()

        print("API check:",response)