import httpx
import json
import time
import asyncio

from rebel.models import (
    AssistantInput,
    AssistantOutput,
    Function,
    ToolCall
)
from rebel.collector import APIClient


class TSAPIClient(APIClient):
    def __init__(self, url: str):
        self.url = url
    
    def request(self, input: AssistantInput) -> AssistantOutput:
        client = httpx.Client(timeout=httpx.Timeout(60.0, read=None))
        
        start_time = time.time()
        actual_output = ""
        tools_called = []
        context = []

        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }

        def stream_and_collect():
            nonlocal actual_output, tools_called, context

            data = {
                'messages': [{'role': message.role, 'content': message.content} for message in input.messages],
                **input.api_params
            }
            
            with client.stream(
                "POST", 
                self.url, 
                json=data,
                headers=headers
            ) as response:
                if response.status_code != 200:
                    # Read the error response content properly
                    error_content = response.read()
                    raise Exception(f"API request failed with status {response.status_code}: {error_content.decode()}")

                # Process the streaming response
                for line in response.iter_lines():
                    if not line:
                        continue

                    if line.startswith("data: "):
                        data_str = line[6:]  # Remove "data: " prefix

                        if data_str.strip() == "[DONE]":
                            break

                        try:
                            data = json.loads(data_str)
                            # Extract text content
                            if "choices" in data and len(data["choices"]) > 0:
                                choice = data["choices"][0]
                                delta = choice.get("delta", {})

                                # Handle assistant content
                                if delta.get("role") == "assistant" and "content" in delta:
                                    if delta["content"]:
                                        actual_output += delta["content"]

                                if delta.get("role") == "tool" and "content" in delta:
                                    if delta["content"]:
                                        context.append(delta["content"])

                                # Handle tool calls
                                if "tool_calls" in delta and delta["tool_calls"]:
                                    for tool_call in delta["tool_calls"]:
                                        tools_called.append(ToolCall(
                                            id=tool_call["id"],
                                            type=tool_call["type"],
                                            function=Function(
                                                name=tool_call["function"]["name"],
                                                arguments=tool_call["function"]["arguments"]
                                            )
                                        ))

                        except json.JSONDecodeError:
                            # Skip malformed JSON lines
                            continue

        # Execute the streaming collection
        stream_and_collect()

        completion_time = time.time() - start_time
        
        return AssistantOutput(
            output=actual_output.strip(),
            tools_called=tools_called,
            context=context,
            execution_time=completion_time
        )
