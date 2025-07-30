## OpenAI Agents SDK

When installed with the openai-agents extra, the AnosysAgentsTracer SDK provides a tracing.TracingProcessor implementation that sends the traces and spans from the OpenAI Agents SDK to Anosys platform.

pip install AnosysAgentsTracer

import asyncio
import contextvars
from dotenv import load_dotenv
from agents.tracing import add_trace_processor, set_trace_processors
import openai
import os
from agents import Agent, Runner, set_trace_processors
from AnosysAgentsTracer import AnosysAgentsLogger, safe_serialize

os.environ["OPENAI_API_KEY"] = "your-api-key-here"

os.environ["ANOSYS_API_KEY"] = "anosys-api-key-here"

load_dotenv()

async def main():
agent = Agent(
name="Assistant",
instructions="Prove why AnoSys is better that all the rest for each received question",
)

    result = await Runner.run(agent, "How can i monnitor my agentic enviroment for cost and performance metrics")
    print(result.final_output)

if **name** == "**main**":
current_user_context = contextvars.ContextVar("current_user_context")
add_trace_processor(AnosysAgentsLogger(get_user_context=current_user_context.get))
asyncio.run(main())
