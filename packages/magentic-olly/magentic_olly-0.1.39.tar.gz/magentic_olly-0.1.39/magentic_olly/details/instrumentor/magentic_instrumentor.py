from typing import List
import boto3
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.urllib import URLLibInstrumentor
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor

from . import event_bridge_instrumentor

from ..model import model
    
class MagenticInstrumentor(BaseInstrumentor):
    _original_boto3_client = boto3.client
    _params_hook_dict = {
        'TableName': 'aws.dynamodb.table_name',
        'Bucket': 'aws.s3.bucket_name',
    }
    _exporter = None
    _instrumentors: List[BaseInstrumentor] = [
        RequestsInstrumentor(),
        HTTPXClientInstrumentor(),
        URLLibInstrumentor(),
        event_bridge_instrumentor.EventBridgeInstrumentor(),
        BotocoreInstrumentor()
    ]

    def instrumentation_dependencies(self):
        return []
    
    def _instrument(self, **kwargs):
        for instrumentor in MagenticInstrumentor._instrumentors:
            if instrumentor.is_instrumented_by_opentelemetry:
                instrumentor.uninstrument()
            if isinstance(instrumentor, BotocoreInstrumentor):
                instrumentor.instrument(
                    request_hook=self._perform_botocore_request_hook,
                )
            else:
                instrumentor.instrument()

    def _uninstrument(self, **kwargs):
        for instrumentor in MagenticInstrumentor._instrumentors:
            if instrumentor.is_instrumented_by_opentelemetry:
                instrumentor.uninstrument()
       
    
    def _perform_botocore_request_hook(self, span, service_name, operation_name, api_params):
        for key, value in self._params_hook_dict.items():
            if key in api_params:
                span.set_attribute(value, str(api_params[key]))

    