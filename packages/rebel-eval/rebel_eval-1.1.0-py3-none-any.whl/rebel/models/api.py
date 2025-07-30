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
    id: str = ''
    type: Literal['function'] = 'function'
    function: Function
    
    def __init__(self, **data):
        # Handle both patterns in __init__
        if 'name' in data and 'input_parameters' in data and 'function' not in data:
            # New pattern: convert to old pattern
            function = Function(
                name=data.pop('name'),
                arguments=json.dumps(data.pop('input_parameters'))
            )
            data['function'] = function
        
        super().__init__(**data)


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
