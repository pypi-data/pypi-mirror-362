from pydantic import BaseModel
from typing import Annotated
from pydantic.functional_serializers import PlainSerializer
from abc import ABC, abstractmethod
from enum import Enum

from rebel.utils.openai_client import OpenAIClientWrapper
from rebel.models import AssistantOutput, AssistantInput


class EvaluationVerdict(str, Enum):
    PASSED = 'passed'
    FAILED = 'failed'
    ERROR = 'error'


class EvaluationResult(BaseModel):
    score: float
    verdict: EvaluationVerdict
    reason: str


class Metric(ABC):
    judge_llm: OpenAIClientWrapper
    
    @abstractmethod
    def measure(
        self,
        input: AssistantInput,
        expected: AssistantOutput,
        actual: AssistantOutput
    ) -> EvaluationResult:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


# custom serialization logic for metric
def serialize_metric(metric: 'Metric') -> dict:
    return {
        'name': metric.get_name(),
        'type': metric.__class__.__name__,
        'module': metric.__class__.__module__
    }

SerializableMetric = Annotated[
    Metric, 
    PlainSerializer(serialize_metric, return_type=dict, when_used='json')
]
