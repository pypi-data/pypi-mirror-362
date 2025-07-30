import logging

from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter, SimpleLogRecordProcessor
 
from . import BaseInitializer
from ..model import model
from ..instrumentor import LoggingInstrumentor
from ..exporter import FilterLogsExporter

class LoggingInitializer(BaseInitializer):
    def __init__(self, params: model.InstrumentationParams):
        super().__init__(params)
        self._processor = BatchLogRecordProcessor(self._create_exporter(),
                                                  schedule_delay_millis=500,
                                                  export_timeout_millis=5000)
        # self._processor = SimpleLogRecordProcessor(self._create_exporter())
        self._instrumentor = LoggingInstrumentor()
    
    def initialize(self):
        self._create_logging_provider()
        if not self._instrumentor.is_instrumented_by_opentelemetry:
            self._instrumentor.instrument()

    def _create_logging_provider(self):
        resource = self._create_resource(self._params.service_name)
        logger_provider = LoggerProvider(resource=resource)
        
       
        logger_provider.add_log_record_processor(
            self._processor
        )

        set_logger_provider(logger_provider)
        
    def force_flush(self):
        self._processor.force_flush()
        
    def _create_exporter(self):
        if self._params.export_mode == model.ExportMode.CONSOLE:
            return ConsoleLogExporter()
        return FilterLogsExporter(
            endpoint=f"{self._params.export_server_url}/v1/logs", 
            headers={"Authorization": f"Bearer {self._params.export_server_token}"}
        )
        
