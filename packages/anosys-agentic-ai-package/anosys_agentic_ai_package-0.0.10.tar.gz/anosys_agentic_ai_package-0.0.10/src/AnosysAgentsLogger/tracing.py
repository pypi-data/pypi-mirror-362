
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
from datetime import datetime
import requests

# Prevent re-initialization
_lock = threading.Lock()
log_api_url="https://www.anosys.ai"

def _to_millis(dt_str):
    if not dt_str:
        return None
    try:
        return int(datetime.fromisoformat(dt_str).timestamp() * 1000)
    except ValueError:
        return None

key_to_cvs = {
  "name": "cvs50",
  "trace_id": "cvs51",
  "span_id": "cvs52",
  "trace_state": "cvs53",
  "parent_id": "cvs54",
  "start_time": "cvs55",
  "cvi1": "cvs56",
  "end_time": "cvs57",
  "cvi2": "cvs58",
  "llm_tools": "cvs59",
  "llm_token_count": "cvs60",
  "llm_output_messages": "cvs61",
  "llm_input_messages": "cvs62",
  "llm_model_name": "cvs63",
  "llm_invocation_parameters": "cvs64",
  "input": "cvs65",
  "output": "cvs66",
  "tool": "cvs67",
  "kind": "cvs68"
}

def reassign(data, starting_index=50):
    global key_to_cvs
    cvs_vars = {}

    # If input is a JSON string, parse it
    if isinstance(data, str):
        data = json.loads(data)

    if not isinstance(data, dict):
        raise ValueError("Input must be a dict or JSON string representing a dict")

    cvs_index = starting_index

    for key, value in data.items():
        if key not in key_to_cvs:
            key_to_cvs[key] = f"cvs{cvs_index}"
            cvs_index += 1
        cvs_var = key_to_cvs[key]
        cvs_vars[cvs_var] = str(value)

    return cvs_vars

def extract_span_info(span):
    variables = {}

    def assign(variable,var_value):
        variables[f'{variable}'] = str(var_value)
    # Top-level keys
    assign('name',span.get('name'))
    assign('trace_id',span.get('context', {}).get('trace_id'))
    assign('span_id',span.get('context', {}).get('span_id'))
    assign('trace_state',span.get('context', {}).get('trace_state'))
    assign('parent_id',span.get('parent_id'))
    assign('start_time',span.get('start_time'))
    assign('cvi1',_to_millis(span.get('start_time')))
    assign('end_time',span.get('end_time'))
    assign('cvi2',_to_millis(span.get('end_time')))

    # Attributes (stringify if nested)
    attributes = span.get('attributes', {})

    assign('llm_tools',json.dumps(attributes.get('llm', {}).get('tools'), ensure_ascii=False))
    assign('llm_token_count',json.dumps(attributes.get('llm', {}).get('token_count'), ensure_ascii=False))
    assign('llm_output_messages',json.dumps(attributes.get('llm', {}).get('output_messages', {}).get('output_messages'), ensure_ascii=False))
    assign('llm_input_messages',json.dumps(attributes.get('llm', {}).get('input_messages', {}).get('input_messages'), ensure_ascii=False))
    assign('llm_model_name',attributes.get('llm', {}).get('model_name'))
    assign('llm_invocation_parameters',json.dumps(attributes.get('llm', {}).get('invocation_parameters'), ensure_ascii=False))
    
    assign('input',json.dumps(attributes.get('input', {}).get('value'), ensure_ascii=False))
    assign('output',json.dumps(attributes.get('output', {}).get('value'), ensure_ascii=False))
    assign('tool',json.dumps(attributes.get('tool', {}), ensure_ascii=False))
    assign('kind',attributes.get('fi', {}).get('span', {}).get('kind'))

    return(reassign(variables))
    # return variables


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

class CustomConsoleExporter(SpanExporter):
    def export(self, spans) -> SpanExportResult:
        for span in spans:
            span_json = json.loads(span.to_json(indent=2))
            deserialized = deserialize_attributes(span_json)
            # print(log_api_url)
            # print(extract_span_info(deserialized))
            requests.post(log_api_url, json=extract_span_info(deserialized), timeout=5)
            # print(json.dumps(deserialized, indent=2))
            # print(span.to_json(indent=2))
        return SpanExportResult.SUCCESS

# class CustomConsoleExporter(SpanExporter):
#     def export(self, spans) -> SpanExportResult:
#         for span in spans:
#             print("=" * 60)
#             print(f"🟢 Span Name: {span.name}")
#             print(f"🕒 Start Time: {span.start_time}")
#             print(f"🕒 End Time:   {span.end_time}")
#             print("🏷️ Attributes:")
#             for key, value in span.attributes.items():
#                 print(f"   • {key}: {value}")
#             print(f"📍 Status: {span.status.status_code.name}")
#             if span.status.description:
#                 print(f"   ↪ {span.status.description}")
#             print("=" * 60 + "\\n")
#         return SpanExportResult.SUCCESS

def setup_tracing(api_url):
    global log_api_url
    log_api_url = api_url

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

        print("[TRACE-DEBUG] AnoSys Instrumented OpenAI agents with custom tracer")

