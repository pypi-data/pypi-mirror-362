from opentelemetry.trace import SpanKind
from opentelemetry.sdk.trace.export import SpanExportResult
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

class FilterExporter(OTLPSpanExporter):
    def export(self, spans) -> SpanExportResult:
        try:
            return self._export_traces(spans)
        except Exception as e:
            print(f"Error exporting traces: {e}")
        return SpanExportResult.FAILURE

    def _export_traces(self, spans) -> SpanExportResult:
        filtered_spans = []
        for span in spans:
            if span.name == "EventBridge.PutEvents" and span.kind == SpanKind.CLIENT:
                continue
            filtered_spans.append(span)
                
        if filtered_spans:
            return super().export(filtered_spans)
        return SpanExportResult.SUCCESS
    
