from pydantic import BaseModel
from typing import List, Optional

from rebel.models import RetryParams, Metric


# the model to define tests
class TestGroup(BaseModel):
    metrics: List[Metric]
    tags: Optional[List[str]] = []
    retry_params: Optional[RetryParams] = RetryParams(count=1) # do not retry by default
    postfix: Optional[str] = None # postfix to basic name of the test (name of the function)
