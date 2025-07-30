from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod

from rebel.utils.openai_client import OpenAIClientWrapper
from rebel.models import (
    Metric,
    AssistantInput,
    AssistantOutput,
    EvaluationResult,
    EvaluationVerdict,
)


class ContextualFScoreTemplate(ABC, BaseModel):
    @abstractmethod
    def generate_claims(actual_output: str) -> str:
        pass

    @abstractmethod
    def generate_truths(
        retrieval_context: str, input_question: str
    ) -> str:
        pass
    
    @abstractmethod
    def generate_hallucination_verdicts(claims: List[str], retrieval_context: str) -> str:
        pass
    
    @abstractmethod
    def generate_completeness_verdicts(truths: List[str], claims: List[str]) -> str:
        pass
    
    @abstractmethod
    def generate_reason(score: float, contradictions: List[str]) -> str:
        pass


class ContextualVerdict(BaseModel):
    verdict: Literal["yes", "idk", "dm", "no"]
    reason: Optional[str] = Field(default=None)


class Verdicts(BaseModel):
    verdicts: List[ContextualVerdict]


class Truths(BaseModel):
    truths: List[str]


class Claims(BaseModel):
    claims: List[str]


class Reason(BaseModel):
    reason: str


class ContextualFScore(Metric):
    beta: float = Field(1.0)
    threshold: float = Field(0.7)
    strict_mode: bool = Field(True)
    model: OpenAIClientWrapper
    template: ContextualFScoreTemplate
    
    
    def measure(
        self,
        input: AssistantInput,
        expected: AssistantOutput,
        actual: AssistantOutput
    ):
        try:
            truths_prompt = self.template.generate_truths(
                retrieval_context=actual.context,
                input_question=input.messages[-1]
            )
            truths = self.model.generate_instructed([{'user': truths_prompt}], Truths)
            
            claims_prompt = self.template.generate_claims(
                actual_output=actual.output
            )
            claims = self.model.generate_instructed([{'user': claims_prompt}], Claims)
            
            hallucination_verdicts_prompt = self.template.generate_hallucination_verdicts(
                claims=claims,
                retrieval_context=actual.context
            )
            hallucination_verdicts = self.model.generate_instructed([{'user': hallucination_verdicts_prompt}], Verdicts)
            
            completeness_verdicts_prompt = self.template.generate_completeness_verdicts(
                truths=truths,
                claims=claims
            )
            completeness_verdicts = self.model.generate_instructed([{'user': completeness_verdicts_prompt}], Verdicts)
            
            scores = self._calculate_score(completeness_verdicts, hallucination_verdicts)
            reason = (
                f"Truths:\n{truths}",
                f"Claims:\n{claims}",
                f"Hallucination Verdicts:\n{hallucination_verdicts}",
                f"Completeness Verdicts:\n{completeness_verdicts}",
                f"Precision: {scores['precision']}",
                f"Recall: {scores['recall']}",
                f"F-Score: {scores['f_score']}",
                f"Score: {scores['score']}",
            )
            
            return EvaluationResult(
                score=scores['score'],
                verdict=EvaluationVerdict.PASSED if scores['score'] >= self.threshold else EvaluationVerdict.FAILED,
                reason=reason
            )
        except Exception as e:
            return EvaluationVerdict(
                score=0.0,
                verdict=EvaluationVerdict.ERROR,
                reason=f'Error during evaluation: {str(e)}'
            )
            

    def _calculate_score(self, completeness_verdicts: Verdicts, hallucination_verdicts: Verdicts) -> Dict[str, float]:
        # claims missed in actual output, but are in the relevant context (incompleteness)
        false_negatives = sum(1 for verdict in completeness_verdicts if verdict.verdict.strip().lower() == 'no')
        # claims shared both in the relevant context and in the actual output
        true_positives = sum(1 for verdict in hallucination_verdicts if verdict.verdict.strip().lower() != 'no')
        # claims from the actual output, but contradictive to context (hallucinations) 
        false_positives = sum(1 for verdict in hallucination_verdicts if verdict.verdict.strip().lower() == 'no')
        
        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives)
        f_score = (1 + self.beta ** 2) * precision * recall / ((self.beta ** 2 * precision) + recall)

        return {
            'precision': precision,
            'recall': recall,
            'f_score': f_score,
            'score': 0 if self.strict_mode and f_score < self.threshold else f_score
        }

    def get_name(self):
        return 'Contextual F-score'
