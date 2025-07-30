
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from .tracing import setup_tracing

# Load environment variables
load_dotenv()
_tracing_initialized = False

def span2json(span):
    data = span.get("data", {})
    object_ = data.get("object")
    id_ = data.get("id")
    trace_id = data.get("trace_id")
    parent_id = data.get("parent_id")
    started_at = data.get("started_at")
    ended_at = data.get("ended_at")
    error = data.get("error")
    span_data = data.get("span_data", {})

    timestamp = span.get("timestamp")
    user_context = json.dumps(span.get("user_context", {}))  # stringify JSON

    def to_millis(dt_str):
        if not dt_str:
            return None
        try:
            # Match JS Date parsing with .slice(0, 23)
            dt = datetime.fromisoformat(dt_str[:23])
            return int(dt.timestamp() * 1000)
        except ValueError:
            return None

    obj = {
        "cvs1": timestamp,
        "g1": to_millis(timestamp),
        "cvs2": user_context,
        "cvs3": data.get("object"),
        "cvs4": data.get("id"),
        "cvs5": data.get("trace_id"),
        "cvs6": data.get("parent_id"),
        "cvs7": data.get("started_at"),
        "cvi1": to_millis(data.get("started_at")),
        "cvs8": data.get("ended_at"),
        "cvi2": to_millis(data.get("ended_at")),
        "cvs9": data.get("error"),
    }

    type_ = span_data.get("type")

    if type_ == "agent":
        return {
            **obj,
            "cvs10": type_,
            "cvs11": span_data.get("name"),
            "cvs12": ", ".join(span_data.get("handoffs", [])),
            "cvs13": ", ".join(span_data.get("tools", [])),
            "cvs14": span_data.get("output_type"),
        }

    elif type_ == "function":
        return {
            **obj,
            "cvs10": type_,
            "cvs11": span_data.get("name"),
            "cvs15": span_data.get("input"),
            "cvs16": span_data.get("output"),
            "cvs17": span_data.get("mcp_data"),
        }

    elif type_ == "guardrail":
        return {
            **obj,
            "cvs10": type_,
            "cvs11": span_data.get("name"),
            "cvs18": span_data.get("triggered"),
        }

    elif type_ == "generation":
        return {
            **obj,
            "cvs10": type_,
            "cvs15": span_data.get("input"),
            "cvs16": span_data.get("output"),
            "cvs19": span_data.get("model"),
            "cvs20": span_data.get("model_config"),
            "cvs21": span_data.get("usage"),
        }

    elif type_ == "custom":
        return {
            **obj,
            "cvs10": type_,
            "cvs11": span_data.get("name"),
            "cvs22": span_data.get("data"),
        }

    elif type_ == "transcription":
        input_ = span_data.get("input", {})
        return {
            **obj,
            "cvs10": type_,
            "cvs22": input_.get("data"),
            "cvs23": input_.get("format"),
            "cvs16": span_data.get("output"),
            "cvs19": span_data.get("model"),
            "cvs20": span_data.get("model_config"),
        }

    elif type_ == "speech":
        output_ = span_data.get("output", {})
        return {
            **obj,
            "cvs10": type_,
            "cvs15": span_data.get("input"),
            "cvs22": output_.get("data"),
            "cvs23": output_.get("format"),
            "cvs19": span_data.get("model"),
            "cvs20": span_data.get("model_config"),
            "cvs24": span_data.get("first_content_at"),
        }

    elif type_ == "speechgroup":
        return {
            **obj,
            "cvs10": type_,
            "cvs15": span_data.get("input"),
        }

    elif type_ == "MCPListTools":
        return {
            **obj,
            "cvs10": type_,
            "cvs25": span_data.get("server"),
            "cvs26": span_data.get("result"),
        }

    elif type_ == "response":
        return {
            **obj,
            "cvs10": type_,
            "cvs27": span_data.get("response_id"),
        }

    elif type_ == "handoff":
        return {
            **obj,
            "cvs10": type_,
            "cvs28": span_data.get("from_agent"),
            "cvs29": span_data.get("to_agent"),
        }

    else:
        print("Warning: Unknown span_data type:", type_)
        return {**obj, "cvs10": type_}


def safe_serialize(obj):
    try:
        if isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        elif isinstance(obj, list):
            return [safe_serialize(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: safe_serialize(v) for k, v in obj.items()}
        elif hasattr(obj, 'dict'):
            return safe_serialize(obj.dict())
        elif hasattr(obj, 'export'):
            return safe_serialize(obj.export())
        elif hasattr(obj, '__dict__'):
            return safe_serialize(vars(obj))
        else:
            return str(obj)
    except Exception as e:
        return f"[Unserializable: {e}]"

class AnosysLogger:
    def __init__(self, get_user_context=None):
        global _tracing_initialized
        _tracing_initialized = False
        api_key = os.getenv('ANOSYS_API_KEY', 'anosys_api_key')
        parts = api_key.split("_")
        while len(parts) < 3:
            parts.append("default") # Pad the list with default values if needed
        part1, part2, part3 = parts[:3]  # take only the first 3
        self.log_api_url = f"https://api.anosys.ai/ingestion/{part1}/{part2}/{part3}"
        self.get_user_context = get_user_context or (lambda: None)

    def _get_session_id(self):
        try:
            # ctx = current_user_context.get()
            user_context = self.get_user_context()
            return getattr(user_context, "session_id", "unknown_session")
        except Exception:
            return "unknown_session"

    def _get_token(self):
        try:
            # ctx = current_user_context.get()
            user_context = self.get_user_context()
            return getattr(user_context, "token", None)
        except Exception:
            return None

    def _log_summary(self, session_id, data):
        try:
            formatted_data = json.loads(json.dumps(data, default=str))
            payload = {
                "timestamp": datetime.utcnow().isoformat(),
                "data": formatted_data,
            }
            # 🔐 Inject user context if available
            user_context = self.get_user_context()
            if user_context:
                payload["user_context"] = {
                    "session_id": getattr(user_context, "session_id", "unknown_session"),
                    "token": getattr(user_context, "token", None),
                    "metadata": None,
                }
            print(self.log_api_url)
            print(span2json(payload))
            # Optionally: send via requests.post(self.log_api_url, json=payload, timeout=5)

        except Exception as e:
            print(f"[Logger] Error logging full trace: {e}")

    def on_trace_start(self, trace):
        global _tracing_initialized
        if not _tracing_initialized:
            print("[TRACE-DEBUG] Not initialized yet — setting up tracing")
            setup_tracing()
            _tracing_initialized = True
        else:
            print("[TRACE-DEBUG] Already initialized — skipping setup")
        session_id = self._get_session_id()
        serialized_data = safe_serialize(trace)
        self._log_summary(session_id, serialized_data)

    def on_trace_end(self, trace):
        session_id = self._get_session_id()
        serialized_data = safe_serialize(trace)
        self._log_summary(session_id, serialized_data)

    def on_span_start(self, span):
        session_id = self._get_session_id()
        serialized_data = safe_serialize(span)
        self._log_summary(session_id, serialized_data)

    def on_span_end(self, span):
        session_id = self._get_session_id()
        serialized_data = safe_serialize(span)
        self._log_summary(session_id, serialized_data)

    

