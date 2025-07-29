from functools import wraps
import sys
from .details.model import model
from .details import wrapper_service, initializer

def magentic_wrapper(func):
    @wraps(func)
    def wrapper(event, context=None, *args, **kwargs):
        service_params = wrapper_service.MagenticWrapperServiceParams(
            event=event,
            lambda_context=context
        )
        
        magentic_service = wrapper_service.MagenticWrapperService(service_params)
        response = magentic_service.run_lambda_handler(func, *args, **kwargs)
        return response
    
    return wrapper

def initialize(params: model.InstrumentationParams):
    tracing_initializer = initializer.InitializerProvider.create_tracing_initializer(params)
    tracing_initializer.initialize()
    print("OpenTelemetry tracing initialized.")
    if params.enable_logging:
        logging_initializer = initializer.InitializerProvider.create_logging_initializer(params)
        logging_initializer.initialize()
        print("OpenTelemetry logging initialized.")
    
def _is_pytest():
    return "pytest" in sys.modules
