from . import TracingInitializer, LoggingInitializer
from ..model import model

class InitializerProvider:
    _tracing_initializer = None
    _logging_initializer = None 
    @classmethod
    def create_tracing_initializer(cls, params: model.InstrumentationParams):
        cls._tracing_initializer = TracingInitializer(params)
        return cls._tracing_initializer

    @classmethod
    def get_tracing_initializer(cls) -> TracingInitializer:
        return cls._tracing_initializer
    
    @classmethod
    def create_logging_initializer(cls, params: model.InstrumentationParams):
        cls._logging_initializer = LoggingInitializer(params)
        return cls._logging_initializer
    
    @classmethod
    def get_logging_initializer(cls) -> LoggingInitializer:
        return cls._logging_initializer
    
    
