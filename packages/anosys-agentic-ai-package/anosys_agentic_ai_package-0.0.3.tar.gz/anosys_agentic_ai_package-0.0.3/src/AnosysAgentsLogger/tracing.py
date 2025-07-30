
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    SpanExporter,
    SpanExportResult,
)
from traceai_openai_agents import OpenAIAgentsInstrumentor
import threading
import json

# Prevent re-initialization
_lock = threading.Lock()

class CustomConsoleExporter(SpanExporter):
    def export(self, spans) -> SpanExportResult:
        for span in spans:
            print("=" * 60)
            print(f"🟢 Span Name: {span.name}")
            print(f"🕒 Start Time: {span.start_time}")
            print(f"🕒 End Time:   {span.end_time}")
            print("🏷️ Attributes:")
            for key, value in span.attributes.items():
                print(f"   • {key}: {value}")
            print(f"📍 Status: {span.status.status_code.name}")
            if span.status.description:
                print(f"   ↪ {span.status.description}")
            print("=" * 60 + "\\n")
        return SpanExportResult.SUCCESS

def set_nested(obj, path, value):
    parts = path.split(".")
    current = obj
    for i, part in enumerate(parts[:-1]):
        try:
            idx = int(part)
            if not isinstance(current, list):
                current_parent = current
                current = []
                if isinstance(current_parent, dict):
                    current_parent[parts[i - 1]] = current
            while len(current) <= idx:
                current.append({})
            current = current[idx]
        except ValueError:
            if part not in current or not isinstance(current[part], (dict, list)):
                current[part] = {}
            current = current[part]
    final_key = parts[-1]
    try:
        final_key = int(final_key)
        if not isinstance(current, list):
            current_parent = current
            current = []
            if isinstance(current_parent, dict):
                current_parent[parts[-2]] = current
        while len(current) <= final_key:
            current.append(None)
    except ValueError:
        pass
    # Try JSON parsing
    if isinstance(value, str) and value.strip().startswith(("{", "[")):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            pass
    if isinstance(final_key, int):
        current[final_key] = value
    else:
        current[final_key] = value

def deserialize_attributes(obj):
    flat_attrs = obj.get("attributes", {})
    new_attrs = {}
    for key, value in flat_attrs.items():
        set_nested(new_attrs, key, value)
    obj["attributes"] = new_attrs
    return obj

# class CustomConsoleExporter(SpanExporter):
#     def export(self, spans) -> SpanExportResult:
#         for span in spans:
#             span_json = json.loads(span.to_json(indent=2))
#             deserialized = deserialize_attributes(span_json)
#             print(json.dumps(deserialized, indent=2))
#             # print(span.to_json(indent=2))
#         return SpanExportResult.SUCCESS

def setup_tracing():
    with _lock:
        print("[TRACE-DEBUG] setup_tracing() called")

        # Setup provider + console exporter
        trace_provider = TracerProvider()
        trace_provider.add_span_processor(SimpleSpanProcessor(CustomConsoleExporter()))
        trace.set_tracer_provider(trace_provider)

        # Re-instrument OpenAI agents safely
        instrumentor = OpenAIAgentsInstrumentor()
        try:
            instrumentor.uninstrument()
        except Exception as e:
            print(f"[TRACE-DEBUG] Uninstrument error (safe to ignore if first call): {e}")
        instrumentor.instrument(tracer_provider=trace_provider)

        print("[TRACE-DEBUG] Instrumented OpenAI agents with custom tracer")

