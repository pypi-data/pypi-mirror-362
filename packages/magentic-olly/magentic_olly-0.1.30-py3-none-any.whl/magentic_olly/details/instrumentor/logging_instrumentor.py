import logging
from opentelemetry._logs import get_logger_provider
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.sdk._logs import LoggingHandler
from opentelemetry.instrumentation.logging import LoggingInstrumentor as InjectLoggingInstrumentor

class LoggingInstrumentor(BaseInstrumentor):
    _original_get_logger = logging.getLogger
    _trace_inject_instrumentor = InjectLoggingInstrumentor()
    _handler_name = 'magentic-logging-handler'
    
    def instrumentation_dependencies(self):
        return []
    
    def _instrument(self, **kwargs):
        logging.getLogger = self._instrumented_get_logger
        if not self._trace_inject_instrumentor.is_instrumented_by_opentelemetry:
            self._trace_inject_instrumentor.instrument()
        
    def _uninstrument(self, **kwargs):
        logging.getLogger = LoggingInstrumentor._original_get_logger
        if self._trace_inject_instrumentor.is_instrumented_by_opentelemetry:
            self._trace_inject_instrumentor.uninstrument()

    def _instrumented_get_logger(self, *args, **kwargs):
        provider = get_logger_provider()
        handler = None
        logger: logging.RootLogger = LoggingInstrumentor._original_get_logger(*args, **kwargs)

        if logger.name and (logger.name == 'root' or logger.name.startswith("opentelemetry")):
            return logger
        
        handler = LoggingHandler(logger_provider=provider)
        handler.name = LoggingInstrumentor._handler_name
        if not any(h.name == LoggingInstrumentor._handler_name for h in logger.handlers):
            logger.addHandler(handler)
        return logger
