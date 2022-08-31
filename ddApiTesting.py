from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.authentication_api import AuthenticationApi
from ddtrace import config, patch_all
import time
from datetime import datetime
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem
from datadog_api_client.exceptions import ForbiddenException
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries
import random



def validate_api():
    ''' Method to Validate API config '''
    try:
        configuration = Configuration()
        with ApiClient(configuration) as api_client:
            api_instance = AuthenticationApi(api_client)
            response = api_instance.validate()

            if response.valid == True:
                print("API check:",response)
    
    except ForbiddenException:
        print("Bad api key, exiting script")
        quit()

def log_call():
    global response
    body = HTTPLog(
        [
            HTTPLogItem(
                ddsource="Python script",
                hostname="zstall-tester",
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

    return response

def metric_call():
    randomNumber = round(random.random())
    body =  MetricPayload(
                series=[
                    MetricSeries(
                        tags=["env:denver"],
                        metric="zstallTester.metric",
                        type=MetricIntakeType(1),
                        points=[
                            MetricPoint(
                                timestamp=int(datetime.now().timestamp()),
                                value=randomNumber,
                            ),
                        ],
                        resources=[
                            MetricResource(
                                name="dummy",
                                type="unit"
                            )
                        ]
                    ),
                ],
            )

    configuration = Configuration()
    with ApiClient(configuration) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.submit_metrics(body=body)
    return response

def main():

    # from ddtrace.opentracer import Tracer, set_global_tracer
    patch_all()
    print('###################################################################################')
    validate_api()
    print('###################################################################################')
    # Get user input
    print()
    get_function_script = int(input( 'Select what to send to DD: [1] Logs [2] Metrics [3] Both:  '))
    function_frequency = int(input( 'Input frequency in seconds: '))
    function_run_time = int(input( 'Total time to run script in minutes: '))
    print()
    
    total_frequence = 0
    # Validate that the api can make calls to DD
    
    if get_function_script == 1:
        print("Running log scritp with interval: " + str(function_frequency))
        print("Valid logs submission will return -> {}")
        time.sleep(.8)

        while (function_run_time * 60) > total_frequence:
            time.sleep(function_frequency)
            total_frequence += function_frequency
            response = log_call()
            print(response, "timestamp:", datetime.now().time())

    elif get_function_script == 2:
        print("Running metric scritp with interval: " + str(function_frequency))
        print("Valid responses look like -> {'errors': []}")
        time.sleep(.8)
        
        while (function_run_time * 60) > total_frequence:
            time.sleep(function_frequency)
            total_frequence += function_frequency
            response = metric_call()
            print(response, "timestamp:", datetime.now().time())

    elif get_function_script == 3:
        print("Running log and metric scripts at interval: " + str(function_frequency))
        print("Valid response will look like: ")
        print("     {} timestamp: ##:##:##.#######")
        print("     {'errors': []} timestamp: ##:##:##.###### ")

        while (function_run_time * 60) > total_frequence:
            time.sleep(function_frequency)
            total_frequence += function_frequency
            log_response = log_call()
            metric_response = metric_call()

            print(log_response, "timestamp:", datetime.now().time())
            print(metric_response, "timestamp:", datetime.now().time())

    else:
        print("Bad entry, rerun script.")

if __name__=="__main__":
    main()