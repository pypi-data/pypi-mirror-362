import os
from enum import Enum
from typing import List, Optional
from typing import Optional
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor


class ExportMode(Enum):
    CONSOLE = "CONSOLE"
    HTTP = "HTTP"
    GRPC = "GRPC"
    
class InstrumentationParams:
    def __init__(
        self,
        service_name: str,
        export_server_url: Optional[str] = None,
        export_server_token: Optional[str] = None,
        export_mode: Optional[ExportMode] = None,
        extra_instrumentors: Optional[List[BaseInstrumentor]] = None,
        enable_logging: Optional[bool] = False,
    ):
        self.service_name = service_name
        self.export_server_url = export_server_url
        self.export_server_token = export_server_token
        self.extra_instrumentors = extra_instrumentors if extra_instrumentors is not None else []
        self.enable_logging = enable_logging

        if export_server_url is None:
            self.export_mode = ExportMode.CONSOLE
        else:
            self.export_mode = export_mode if export_mode is not None else ExportMode.HTTP

