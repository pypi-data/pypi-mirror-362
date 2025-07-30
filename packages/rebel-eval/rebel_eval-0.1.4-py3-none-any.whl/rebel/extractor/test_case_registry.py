from typing import List, Optional, Dict

from rebel.models import (
    TestSuite,
    Message,
    ParameterGrid,
    AssistantOutput,
)


test_suites: List[TestSuite] = []


# decorator to define benchmark tests in the code
def test_case(
    messages: List[Message],
    api_params: Optional[Dict],
    param_grid: ParameterGrid,
    expected_output: AssistantOutput,
):
    def decorator(func):
        name = func.__name__
        
        test_suites.extend([
            TestSuite(
                name=name,
                messages=messages,
                api_params=api_params,
                parameter_grid=param_grid,
                expected_output=expected_output,
                retry_params=group.retry_params,
                metrics=group.metrics
            ) for group in func()
        ])     
        
        return func
        
    return decorator
