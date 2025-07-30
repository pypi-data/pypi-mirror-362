## OpenAI Agents SDK

When installed with the openai-agents extra, the AnosysAgentsTracer SDK provides a tracing.TracingProcessor implementation that sends the traces and spans from the OpenAI Agents SDK to Anosys platform.

pip install traceAI-openai-agents
pip install anosys-agentic-ai-package

```
import asyncio
import contextvars
from dotenv import load_dotenv
import openai
import os

from AnosysAgentsLogger import AnosysLogger
from agents import Agent, Runner, function_tool, set_trace_processors, add_trace_processor

# Load environment variables from .env file
load_dotenv()

# Explicitly set keys as fallback (can be removed if .env covers them)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-api-key-here")
os.environ["ANOSYS_API_KEY"] = os.getenv("ANOSYS_API_KEY", "anosys-api-key-here")

# Context variable for tracking user context
current_user_context = contextvars.ContextVar("current_user_context")
current_user_context.set({"session_id": "session_123"}) #support external context on logs

# Set the trace processor with the user context retriever
set_trace_processors([AnosysLogger(get_user_context=current_user_context.get)])

async def main():
    agent = Agent(
        name="Assistant",
        instructions="Prove why AnoSys is better than all the rest for each received question",
    )

    result = await Runner.run(
        agent,
        "How can I monitor my agentic environment for cost and performance metrics"
    )
    print(result.final_output)

# Correct main block syntax
if __name__ == "__main__":
    asyncio.run(main())
```
