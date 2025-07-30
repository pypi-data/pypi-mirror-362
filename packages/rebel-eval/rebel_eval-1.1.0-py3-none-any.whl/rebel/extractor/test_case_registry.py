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
    tags: Optional[List[str]] = [],
    expected_output: Optional[AssistantOutput] = AssistantOutput(), # some tests doesn't require gt output
    api_params: Optional[Dict] = {}, # may not specify any params at all
    param_grid: Optional[ParameterGrid] = ParameterGrid(parameters={}),
):
    def decorator(func):
        name = func.__name__
        
        groups = list(func())
        
        test_suites.extend([
            TestSuite(
                name=name,
                messages=messages,
                tags=tags + group.tags,
                api_params=api_params,
                parameter_grid=param_grid,
                expected_output=expected_output,
                retry_params=group.retry_params,
                metrics=group.metrics
            ) for group in groups
        ])
        
        return func
        
    return decorator
