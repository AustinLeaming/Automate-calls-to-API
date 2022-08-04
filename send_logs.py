"""
Send deflate logs returns "Request accepted for processing (always 202 empty JSON)." response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem

response = "null"

def make_call():
    global response
    body = HTTPLog(
        [
            HTTPLogItem(
                ddsource="Python",
                hostname="Python script",
                message="filled in tag",
                service="payment",
                env="test",
                ddtags="env:test,location:denver"
            ),
        ]
    )

    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = LogsApi(api_client)
        response = api_instance.submit_log(content_encoding=ContentEncoding("deflate"), body=body)

