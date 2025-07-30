from pydantic import BaseModel
from typing import List

from rebel.models import (
    TestAttemptExecuted,
    SerializableMetric,
    EvaluationResult,
    AssistantOutput,
    TestCase
)


# Each test attemps is evaluated by a bunch of metrics,
# this model specifies the metric will be used in this evaluation
class EvaluationAttempt(TestAttemptExecuted):
    metric: SerializableMetric


# Evaluation attempt with result of metric calculation
class EvaluationAttemptEvaluated(EvaluationAttempt):
    evaluation_result: EvaluationResult


# Initial test case before unfolding to retries with aggregated result
# + result for each attempt
class TestCaseEvaluated(TestCase):
    actual_outputs: List[AssistantOutput]
    evaluation_results: List[EvaluationResult]
    aggregated_result: EvaluationResult
