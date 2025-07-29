import logging
from opentelemetry import propagate, trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor
from opentelemetry.trace import SpanKind, Status, StatusCode, get_tracer_provider

from .exporter import filter_spans_exporter
from .wrapper_params import MagenticWrapperServiceParams
from .utils import constants
from .utils.spans import SpansUtils
from .initializer import InitializerProvider

logger = logging.getLogger(__name__)

class MagenticWrapperService:
    
    def __init__(self, params: MagenticWrapperServiceParams):
        self._params:MagenticWrapperServiceParams = params
        self._current_otel_context = self._params.otel_context
        self._client_handler = _ClientHandler(self._params)
        self._tracing_initializer = InitializerProvider.get_tracing_initializer()
        self._logging_initializer = InitializerProvider.get_logging_initializer()
        self._is_lambda_executed = False

    def run_lambda_handler(self, func, *args, **kwargs):
        try:
            response = self._run_lambda_handler(func, *args, **kwargs)
        except Exception as e:
            logger.error(f"Wrapper service error: {e}")
            
        if not self._is_lambda_executed:
            response = self._execute_lambda(func, args, kwargs)  
        
        self._is_lambda_executed = False
        return response
        
    def _run_lambda_handler(self, func, *args, **kwargs):
        self._perform_pre_processing()
        
        response = {}
        with self._create_service_span_context_manager(func.__name__) as service_span:
            response = self._execute_lambda(func, args, kwargs)
            if response is None:
                response = {}
            self._set_span_attributes(service_span, response)
            self._inject_tracing_context(response)
            
        response = self._perform_post_processing(response)
        return response

    def _execute_lambda(self, func, args, kwargs):
        response = func(self._params.payload, self._params.lambda_context, *args, **kwargs)
        self._is_lambda_executed = True
        return response
            

    def _perform_pre_processing(self):
        self._client_handler.handle_spans()
        
        self._current_otel_context = self._client_handler.get_context()
        
        self._create_current_service_resource()
    
    def _perform_post_processing(self, response):
        self._client_handler.end_spans(response)
        self._tracing_initializer.force_flush()
        if self._logging_initializer:
            self._logging_initializer.force_flush()
        return response
        
    def _should_create_client_spans(self):
        return self._params.has_client_service_name and not self._params.is_event_bridge_event

    
        
    def _create_client_span(self):
        if not self._params.has_client_service_name:
            return None
        client_tracer = trace.get_tracer(__name__)
        client_span = client_tracer.start_span("retro-client-span", context=self._current_otel_context, kind=SpanKind.CLIENT)
        self._set_span_resource_attributes(client_span)
        return client_span
    
    def _set_span_attributes(self, service_span, response):
        self._set_span_resource_attributes(service_span)
        self._set_span_magentic_attributes(service_span)
        SpansUtils.set_span_response_attributes(service_span, response)

    def _set_span_resource_attributes(self, span):
        if self._params.has_instance_id:
            span.set_attribute("server.instance.id", str(self._params.instance_id))
            
    def _set_span_magentic_attributes(self, span):
        if not self._params.has_magentic_span_attrs:
            return
        attrs = self._params.magentic_span_attrs
        for key, value in attrs.items():
            span.set_attribute(key, str(value))

    def _create_current_service_resource(self):
        self._tracing_initializer.reset_service_resource()
        self._extend_service_resource_attrs()
    

    def _create_service_span_context_manager(self, func_name):
        service_tracer = trace.get_tracer(__name__)
        span_manager = service_tracer.start_as_current_span(func_name, 
                            context=self._current_otel_context,
                            kind=self._params.service_span_kind)
        return span_manager
    
    def _extend_service_resource_attrs(self):
        resource_attributes = {}
        if self._params.has_instance_id:
            resource_attributes["server.instance.id"] = self._params.instance_id
        if self._params.arn:
            resource_attributes["resource.arn"] = self._params.arn
            resource_attributes["resource.platform"] = "AWS"
            resource_attributes["resource.type"] = "Lambda"
        if self._params.account_id:
            resource_attributes["aws.account.id"] = self._params.account_id
        if self._params.region:
            resource_attributes["aws.account.region"] = self._params.region
        self._tracing_initializer.append_service_resource_attrs(resource_attributes)
    

    def _inject_tracing_context(self, response:dict[str, any]):
        if not self._tracing_initializer.propagate_context:
            return
        response.update(self._params.propagation_tracing_context)
        propagator = propagate.get_global_textmap()
        otel_context = {}
        propagator.inject(otel_context)
        response[constants.OTEL_TRACE_CONTEXT_KEY] = otel_context


class _ClientHandler:
    def __init__(self, params: MagenticWrapperServiceParams):
        self._params = params
        self._spans = []
        self._tracing_initializer = InitializerProvider.get_tracing_initializer()
        self._client_service_name = params.client_service_name
        self._current_otel_context = self._params.otel_context
    
    
    def handle_spans(self):
        if self._client_service_name is None:
            return
        self._switch_to_client_resource()
        retro_server_span = self._create_retro_server_span()
        retro_client_span = self._create_retro_client_span()
        if retro_server_span:
            self._spans.append(retro_server_span)
        if retro_client_span:
            self._spans.append(retro_client_span)
            
    def get_context(self):
        return self._current_otel_context
    
    def end_spans(self, response:dict[str, any]):
        for span in reversed(self._spans):
            SpansUtils.set_span_response_attributes(span, response)
            span.end()
            
    def _switch_to_client_resource(self):
        service_name = self._params.client_service_name
        self._tracing_initializer.set_service_resource(service_name)
        if self._params.client_service_arn:
            resource_attributes = {}
            resource_attributes["resource.arn"] = self._params.client_service_arn
            resource_attributes["resource.platform"] = "AWS"
            resource_attributes["resource.type"] = self._params.client_service_type
            self._tracing_initializer.append_service_resource_attrs(resource_attributes, service_name)
        
    def _create_retro_server_span(self):
        if not self._params.should_create_retro_server_span:
            return None
        
        service_tracer = trace.get_tracer(__name__)
        span = service_tracer.start_span("retro-server-span", 
                                                  context=self._current_otel_context, 
                                                  kind=SpanKind.SERVER)
        self._current_otel_context = trace.set_span_in_context(span)
        return span

    def _create_retro_client_span(self):
        if self._client_service_name is None:
            return None
        
        client_tracer = trace.get_tracer(__name__)
        span = client_tracer.start_span("retro-client-span", 
                                                context=self._current_otel_context, 
                                                kind=SpanKind.CLIENT)
        self._current_otel_context = trace.set_span_in_context(span)
        return span
