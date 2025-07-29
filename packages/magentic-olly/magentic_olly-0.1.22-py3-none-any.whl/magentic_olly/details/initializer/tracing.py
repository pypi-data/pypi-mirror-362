from typing import Optional

from opentelemetry import propagate, trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import SpanKind, Status, StatusCode


from . import BaseInitializer
from ..exporter import filter_spans_exporter
from ..instrumentor import magentic_instrumentor
from ..model import model

class TracingInitializer(BaseInitializer):
    def __init__(self, params: model.InstrumentationParams):
        super().__init__(params)
        self._instrumentors = [
            magentic_instrumentor.MagenticInstrumentor()
        ]
        self._processor = self._create_processor()
        self._instrumentors.extend(params.extra_instrumentors)
        self._service_resource = self._create_resource()
        

    def initialize(self):
        self._create_tracer_provider()
        self._instrument_external_libs()
    
    def append_service_resource_attrs(self, attributes: dict, service_name: Optional[str] = None):
        attributes['service.name'] = service_name or self._params.service_name
        self._service_resource = Resource.create(attributes)
        self._create_tracer_provider()
        
    def set_service_resource(self, service_name: Optional[str] = None):
        resource = self._create_resource(service_name)
        self._create_tracer_provider(resource)
        
    def reset_service_resource(self):
        self._create_tracer_provider()
            
    def force_flush(self):
        self._processor.force_flush()
        
    @property
    def service_name(self):
        return self._params.service_name
    
    @property
    def propagate_context(self):
        return self._params.propagate_context

    def _create_tracer_provider(self, resource:Optional[Resource]=None):
        tracer_provider = TracerProvider(resource=resource or self._service_resource)
        tracer_provider.add_span_processor(self._processor)
        trace._TRACER_PROVIDER = tracer_provider


    def _create_processor(self):
        exporter = self._create_exporter()
        processor = BatchSpanProcessor(exporter, max_export_batch_size=5, 
                                       schedule_delay_millis=500,
                                       export_timeout_millis=5000)                
        return processor

    def _create_exporter(self):
        if self._params.export_mode == model.ExportMode.CONSOLE:
            return ConsoleSpanExporter()
        return filter_spans_exporter.FilterExporter(
            endpoint=f"{self._params.export_server_url}/v1/traces", 
            headers={"Authorization": f"Bearer {self._params.export_server_token}"}
        )
    
    def _instrument_external_libs(self):
        for instrumentor in self._instrumentors:
            if instrumentor.is_instrumented_by_opentelemetry:
                instrumentor.uninstrument()
            instrumentor.instrument()
