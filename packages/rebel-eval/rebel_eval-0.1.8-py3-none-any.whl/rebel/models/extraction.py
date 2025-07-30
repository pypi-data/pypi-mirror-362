from pydantic import BaseModel
from typing import List, Optional

from rebel.models import RetryParams, Metric


# the model to define tests
class TestGroup(BaseModel):
    retry_params: RetryParams
    metrics: List[Metric]
    postfix: Optional[str] = None # postfix to basic name of the test (name of the function)
