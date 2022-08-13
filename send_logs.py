"""
Send deflate logs returns "Request accepted for processing (always 202 empty JSON)." response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem
import random

response = "null"
random_key_pair = "null"

def make_call():
    global response
    body = HTTPLog(
        [
            HTTPLogItem(
                ddsource="Python script",
                hostname="send_logs",
                message="Hello world",
                service="payment",
                ddtags="env:test,location:denver",
            ),
        ]
    )

    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = LogsApi(api_client)
        response = api_instance.submit_log(content_encoding=ContentEncoding("deflate"), body=body)

def make_call_random_service():
    random_value=str(random.randrange(0,10000,5))
    global response
    random_number = random.randrange(0,3,1)
    #send a log with a random value for Long, Short, Current - to average in DD later
    #send a log with a random KEY:PAIR
    #FULL:LGOU2
    #FULL:IRC
    #RIC:LGOU2
    #RIC:IRC
    #merge all these into a standard attribute - FULLRIC
    #create facet for new standard attribute
    if random_number == 0:
        body = HTTPLog(
            [
                HTTPLogItem(
                    ddsource="Python script",
                    ddservice="randomized",
                    hostname="send_logs",
                    message="Hello World",
                    FULL="LGOU2",
                    Long=random_value,
                    Short=random_value,
                    Current=random_value
                ),
            ]
        )

        configuration = Configuration()
        with ApiClient(configuration) as api_client:
            api_instance = LogsApi(api_client)
            response = api_instance.submit_log(content_encoding=ContentEncoding("deflate"), body=body)

    if random_number == 1:
        body = HTTPLog(
            [
                HTTPLogItem(
                    ddsource="Python script",
                    ddservice="randomized",
                    hostname="send_logs",
                    message="Hello World -- hello",
                    FULL="IRC",
                    Long=random_value,
                    Short=random_value,
                    Current=random_value
                ),
            ]
        )

        configuration = Configuration()
        with ApiClient(configuration) as api_client:
            api_instance = LogsApi(api_client)
            response = api_instance.submit_log(content_encoding=ContentEncoding("deflate"), body=body)

    if random_number == 2:
        body = HTTPLog(
            [
                HTTPLogItem(
                    ddsource="Python script",
                    ddservice="randomized",
                    hostname="send_logs",
                    message="Hello World -- hello",
                    RIC="LGOU2",
                    Long=random_value,
                    Short=random_value,
                    Current=random_value
                ),
            ]
        )

        configuration = Configuration()
        with ApiClient(configuration) as api_client:
            api_instance = LogsApi(api_client)
            response = api_instance.submit_log(content_encoding=ContentEncoding("deflate"), body=body)

    if random_number == 3:
        body = HTTPLog(
            [
                HTTPLogItem(
                    ddsource="Python script",
                    ddservice="randomized",
                    hostname="send_logs",
                    message="Hello World -- hello",
                    RIC="IRC",
                    Long=random_value,
                    Short=random_value,
                    Current=random_value
                ),
            ]
        )

        configuration = Configuration()
        with ApiClient(configuration) as api_client:
            api_instance = LogsApi(api_client)
            response = api_instance.submit_log(content_encoding=ContentEncoding("deflate"), body=body)

    

