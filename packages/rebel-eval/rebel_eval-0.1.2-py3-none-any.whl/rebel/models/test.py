from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import List, Dict, Any

from rebel.models import AssistantInput, AssistantOutput, SerializableMetric, Message


class RetryAggregationStrategy(str, Enum):
    MIN = 'min'
    MAX = 'max'
    MEAN = 'mean'
    MEDIAN = 'median'


class RetryParams(BaseModel):
    count: int
    aggregation_strategy: RetryAggregationStrategy 


class ParameterGrid(BaseModel):
    parameters: Dict[str, List[Any]]
    
    def expand(self) -> List[Dict[str, Any]]:
        """Generate all parameter combinations"""
        import itertools
        keys = list(self.parameters.keys())
        values = list(self.parameters.values())
        return [dict(zip(keys, combo)) for combo in itertools.product(*values)]


# Suite of tests specified by the user, then unfolds into different api parametrizations
class TestSuite(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True) # to include metric
    
    name: str
    tags: List[str]
    retry_params: RetryParams
    
    messages: List[Message]
    api_params: Dict[str, Any] # suite API parameters
    parameter_grid: ParameterGrid # API parameters grid, higher priority than api_params
    
    expected_output: AssistantOutput
    
    metrics: List[SerializableMetric] # output for each retry will be measured using different metrics


# Basic test case info, common for all retry attempts and evaluations
class TestInfo(BaseModel):
    name: str
    tags: List[str]
    retry_params: RetryParams # need them for post-eval aggregation
    input: AssistantInput
    expected_output: AssistantOutput


# Concrete test case with fixed set of api parameters, drops down into multiple retry attempts
class TestCase(TestInfo):
    model_config = ConfigDict(arbitrary_types_allowed=True) # to include metric
    
    metrics: List[SerializableMetric]

# Each attempt from one test case have similar parametrization and input
class TestAttempt(TestCase):
    number: int # number of the attempt for the case


# Test attempt after execution, almost ready to be evaluated
class TestAttemptExecuted(TestAttempt):
    actual_output: AssistantOutput
