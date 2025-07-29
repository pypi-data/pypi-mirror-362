from opentelemetry.trace import SpanKind, Status, StatusCode

class SpansUtils:
    @staticmethod
    def set_span_response_attributes(span, response):
        status_code = response.get("statusCode", None)
        if status_code is None:
            return
        if isinstance(status_code, int) and status_code >= 400:
            span.set_status(Status(StatusCode.ERROR))
        else:
            span.set_status(Status(StatusCode.OK))
        span.set_attribute("response.status_code", str(status_code))