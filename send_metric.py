"""
Submit metrics returns "Payload accepted" response
"""

from datetime import datetime
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.metrics_api import MetricsApi
from datadog_api_client.v2.model.metric_intake_type import MetricIntakeType
from datadog_api_client.v2.model.metric_payload import MetricPayload
from datadog_api_client.v2.model.metric_point import MetricPoint
from datadog_api_client.v2.model.metric_resource import MetricResource
from datadog_api_client.v2.model.metric_series import MetricSeries

response = "null"

def metric_call():
    global response
    body = MetricPayload(
        series=[
            MetricSeries(
                tags=["env:denver"],
                metric="hello.metric",
                type=MetricIntakeType(1),
                points=[
                    MetricPoint(
                        timestamp=int(datetime.now().timestamp())
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
