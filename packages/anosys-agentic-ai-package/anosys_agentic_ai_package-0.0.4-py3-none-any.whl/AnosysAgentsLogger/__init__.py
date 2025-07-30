# Import required modules
import json
from datetime import datetime
import os
import requests
from dotenv import load_dotenv  # Loads variables from a .env file into environment
from .tracing import setup_tracing  # Assumes custom tracing setup

# Load environment variables from .env file
load_dotenv()
_tracing_initialized = False  # Global flag to ensure tracing setup is only run once

api_key = os.getenv('ANOSYS_API_KEY', 'anosys_api_key')
resolver = f"https://api.anosys.ai/api/resolveapikeys?apikey={api_key}"

def _to_millis(dt_str):
    if not dt_str:
        return None
    try:
        return int(datetime.fromisoformat(dt_str).timestamp() * 1000)
    except ValueError:
        return None


def span2json(span):
    data = span.get("data", {})
    span_data = data.get("span_data", {})
    timestamp = span.get("timestamp")
    user_context = json.dumps(span.get("user_context", {}))

    base = {
        "cvs1": timestamp,
        "g1": _to_millis(timestamp),
        "cvs2": user_context,
        "cvs3": data.get("object"),
        "cvs4": data.get("id"),
        "cvs5": data.get("trace_id"),
        "cvs6": data.get("parent_id"),
        "cvs7": data.get("started_at"),
        "cvi1": _to_millis(data.get("started_at")),
        "cvs8": data.get("ended_at"),
        "cvi2": _to_millis(data.get("ended_at")),
        "cvs9": data.get("error"),
    }

    type_ = span_data.get("type")
    extended = {
        "agent": lambda: {
            "cvs11": span_data.get("name"),
            "cvs12": ", ".join(span_data.get("handoffs", [])),
            "cvs13": ", ".join(span_data.get("tools", [])),
            "cvs14": span_data.get("output_type"),
        },
        "function": lambda: {
            "cvs11": span_data.get("name"),
            "cvs15": span_data.get("input"),
            "cvs16": span_data.get("output"),
            "cvs17": span_data.get("mcp_data"),
        },
        "guardrail": lambda: {
            "cvs11": span_data.get("name"),
            "cvs18": span_data.get("triggered"),
        },
        "generation": lambda: {
            "cvs15": span_data.get("input"),
            "cvs16": span_data.get("output"),
            "cvs19": span_data.get("model"),
            "cvs20": span_data.get("model_config"),
            "cvs21": span_data.get("usage"),
        },
        "custom": lambda: {
            "cvs11": span_data.get("name"),
            "cvs22": span_data.get("data"),
        },
        "transcription": lambda: {
            "cvs22": span_data.get("input", {}).get("data"),
            "cvs23": span_data.get("input", {}).get("format"),
            "cvs16": span_data.get("output"),
            "cvs19": span_data.get("model"),
            "cvs20": span_data.get("model_config"),
        },
        "speech": lambda: {
            "cvs15": span_data.get("input"),
            "cvs22": span_data.get("output", {}).get("data"),
            "cvs23": span_data.get("output", {}).get("format"),
            "cvs19": span_data.get("model"),
            "cvs20": span_data.get("model_config"),
            "cvs24": span_data.get("first_content_at"),
        },
        "speechgroup": lambda: {
            "cvs15": span_data.get("input"),
        },
        "MCPListTools": lambda: {
            "cvs25": span_data.get("server"),
            "cvs26": span_data.get("result"),
        },
        "response": lambda: {
            "cvs27": span_data.get("response_id"),
        },
        "handoff": lambda: {
            "cvs28": span_data.get("from_agent"),
            "cvs29": span_data.get("to_agent"),
        },
    }

    result = {**base, "cvs10": type_}
    if type_ in extended:
        result.update(extended[type_]())
    else:
        logger.warning(f"Unknown span_data type: {type_}")

    return result


def safe_serialize(obj):
    try:
        if isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        elif isinstance(obj, list):
            return [safe_serialize(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: safe_serialize(v) for k, v in obj.items()}
        elif hasattr(obj, "dict"):
            return safe_serialize(obj.dict())
        elif hasattr(obj, "export"):
            return safe_serialize(obj.export())
        elif hasattr(obj, "__dict__"):
            return safe_serialize(vars(obj))
        return str(obj)
    except Exception as e:
        return f"[Unserializable: {e}]"


class AnosysLogger:
    """
    Logging utility that captures traces and spans, transforms them,
    and sends them to the Anosys API endpoint for ingestion/logging.
    """

    def __init__(self, get_user_context=None):
        global _tracing_initialized
        _tracing_initialized = False

        # retrive AnoSys url from API key and build the logging endpoint URL
        try:
            response = requests.get(resolver)
            response.raise_for_status()  # Raises HTTPError for bad responses (e.g., 4xx/5xx)
            data = response.json()
            self.log_api_url = data.get("url", "https://www.anosys.ai")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to resolve API key: {e}")
            self.log_api_url = "https://www.anosys.ai"

        # Optional function to provide user context (e.g., session_id, token)
        self.get_user_context = get_user_context or (lambda: None)

    def _get_session_id(self):
        """Safely retrieves the current session ID from user context."""
        try:
            user_context = self.get_user_context()
            return getattr(user_context, "session_id", "unknown_session")
        except Exception:
            return "unknown_session"

    def _get_token(self):
        """Safely retrieves the current token from user context."""
        try:
            user_context = self.get_user_context()
            return getattr(user_context, "token", None)
        except Exception:
            return None

    def _log_summary(self, session_id, data):
        """
        Logs serialized trace or span data.
        Optionally includes user context metadata.
        """
        try:
            formatted_data = json.loads(json.dumps(data, default=str))
            payload = {
                "timestamp": datetime.utcnow().isoformat(),
                "data": formatted_data,
            }

            user_context = self.get_user_context()
            if user_context:
                payload["user_context"] = {
                    "session_id": getattr(user_context, "session_id", "unknown_session"),
                    "token": getattr(user_context, "token", None),
                    "metadata": None,
                }

            # Debug print (replace with POST request in production)
            # print(self.log_api_url)
            # print(span2json(payload))
            requests.post(self.log_api_url, json=span2json(payload), timeout=5)

        except Exception as e:
            print(f"[Logger] Error logging full trace: {e}")

    def on_trace_start(self, trace):
        """
        Called when a trace begins. Initializes tracing if not already set up.
        """
        global _tracing_initialized
        if not _tracing_initialized:
            print("[TRACE-DEBUG] Not initialized yet — setting up tracing")
            setup_tracing(self.log_api_url)
            _tracing_initialized = True
        else:
            print("[TRACE-DEBUG] Already initialized — skipping setup")

        session_id = self._get_session_id()
        serialized_data = safe_serialize(trace)
        self._log_summary(session_id, serialized_data)

    def on_trace_end(self, trace):
        """Called when a trace ends. Logs final trace state."""
        session_id = self._get_session_id()
        serialized_data = safe_serialize(trace)
        self._log_summary(session_id, serialized_data)

    def on_span_start(self, span):
        """Called when a span starts. Logs initial span data."""
        session_id = self._get_session_id()
        serialized_data = safe_serialize(span)
        self._log_summary(session_id, serialized_data)

    def on_span_end(self, span):
        """Called when a span ends. Logs completed span data."""
        session_id = self._get_session_id()
        serialized_data = safe_serialize(span)
        self._log_summary(session_id, serialized_data)

    def force_flush(self) -> None:
        """Forces flush of all queued spans and traces (no-op)."""
        pass

    def shutdown(self) -> None:
        """Graceful shutdown hook (no-op)."""
        pass
