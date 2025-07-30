from pydantic import BaseModel
from enum import Enum
from typing import Literal, List, Optional, Dict, Any
import json


class RoleEnum(str, Enum):
    user = 'user'
    assistant = 'assistant'
    tool = 'tool'
    system = 'system'


class Function(BaseModel):
    name: str
    arguments: str
    
    def parse_arguments(self) -> Dict[str, Any]:
        return json.loads(self.arguments)

class ToolCall(BaseModel):
    id: str
    type: Literal['function']
    function: Function


class Message(BaseModel):
    role: RoleEnum
    content: str
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None


class AssistantInput(BaseModel):
    messages: List[Message]
    api_params: Dict[str, Any]


class AssistantOutput(BaseModel):
    output: Optional[str] = ''
    tools_called: Optional[List[ToolCall]] = []
    context: Optional[List[str]] = []
    execution_time: Optional[float] = None # None for expected output
