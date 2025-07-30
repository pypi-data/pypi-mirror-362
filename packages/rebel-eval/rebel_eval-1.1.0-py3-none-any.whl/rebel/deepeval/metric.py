from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
from abc import ABC, abstractmethod

from rebel.models import (
    Metric,
    AssistantOutput,
    EvaluationResult,
    AssistantInput,
    EvaluationVerdict
)
from rebel.deepeval.client import OpenAIClientLLM


class DeepevalMetric(Metric, ABC):
    judge_llm: OpenAIClientLLM
    
    def get_name(self):
        raise Exception('not implemented')
    
    @abstractmethod
    def get_deepeval_metric(self) -> BaseMetric:
        pass
    
    def measure(
        self,
        input: AssistantInput,
        expected: AssistantOutput,
        actual: AssistantOutput
    ) -> EvaluationResult:
        metric = self.get_deepeval_metric()
        test_case = convert_to_test_case(input, expected, actual)
        
        score = metric.measure(test_case)
        return EvaluationResult(
            score=score,
            verdict=EvaluationVerdict.PASSED if metric.success else EvaluationVerdict.FAILED,
            reason=metric.reason
        )


def convert_to_test_case(
    input: AssistantInput,
    expected: AssistantOutput,
    actual: AssistantOutput
) -> LLMTestCase:
    return LLMTestCase(
        input=input.messages[0].content,
        actual_output=actual.output,
        expected_output=expected.output,
        context=actual.context,
    )
        