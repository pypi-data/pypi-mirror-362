from abc import ABC, abstractmethod

from rebel.models import AssistantInput, AssistantOutput


class APIClient(ABC):
    @abstractmethod
    def request(self, input: AssistantInput) -> AssistantOutput:
        pass
