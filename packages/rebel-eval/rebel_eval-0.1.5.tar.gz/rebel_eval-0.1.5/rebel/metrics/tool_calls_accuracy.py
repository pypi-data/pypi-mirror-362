import numpy as np
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from sklearn.metrics.pairwise import cosine_similarity
import json
from typing import Dict, Any, List


from rebel.models import (
    ToolCall,
    Metric,
    AssistantInput,
    AssistantOutput,
    EvaluationResult,
    EvaluationVerdict,
)


class ToolCallDistance(ABC, BaseModel):
    @abstractmethod
    def measure(self, first_call: ToolCall, second_call: ToolCall) -> float:
        pass


class ExactMatchToolCallDistance(ToolCallDistance):
    def measure(self, first_call: ToolCall, second_call: ToolCall) -> float:
        # Compare both function name and arguments
        if (first_call.function.name == second_call.function.name and 
            first_call.function.arguments == second_call.function.arguments):
            return 1.0
        return 0.0


class Encoder(ABC, BaseModel):
    def encode(self, texts: List[str]) -> np.ndarray:
        pass


class CosineSimilarityToolCallDistance(ToolCallDistance):
    encoder: Encoder = Field()
    aggregation_method: str = Field(default="mean")  # "mean", "weighted_mean", "min", "max"
    
    def measure(self, first_call: ToolCall, second_call: ToolCall) -> float:
        # First check if function names match
        if first_call.function.name != second_call.function.name:
            return 0.0
        
        # Get parameters dictionaries
        first_params = first_call.function.parse_arguments() or {}
        second_params = second_call.function.parse_arguments() or {}
        
        # If both have no parameters, they're identical
        if not first_params and not second_params:
            return 1.0
        
        # If only one has parameters, they're different
        if not first_params or not second_params:
            return 0.0
        
        # Compare each argument separately
        argument_similarities = self._compare_arguments(first_params, second_params)
        
        # Aggregate the similarities
        return self._aggregate_similarities(argument_similarities)
    
    
    def _compare_arguments(self, first_params: Dict[str, Any], second_params: Dict[str, Any]) -> List[float]:
        """Compare each argument separately using cosine similarity"""
        similarities = []
        
        # Get all unique argument names
        all_keys = set(first_params.keys()) | set(second_params.keys())
        
        for key in all_keys:
            first_value = first_params.get(key)
            second_value = second_params.get(key)
            
            # If argument is missing in one of the calls
            if first_value is None or second_value is None:
                similarities.append(0.0)
                continue
            
            # Convert values to text for encoding
            first_text = self._value_to_text(key, first_value)
            second_text = self._value_to_text(key, second_value)
            
            # Calculate cosine similarity for this argument
            similarity = self._calculate_text_similarity(first_text, second_text)
            similarities.append(similarity)
        
        return similarities
    
    def _value_to_text(self, key: str, value: Any) -> str:
        """Convert argument value to text representation"""
        if isinstance(value, (dict, list)):
            value_str = json.dumps(value, sort_keys=True)
        else:
            value_str = str(value)
        
        return f"{key}: {value_str}"
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two text strings"""
        try:
            # Encode both texts
            vectors = self.encoder.encode([text1, text2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
            
            return float(similarity)
        except Exception as e:
            # Fallback to exact match if encoding fails
            return 1.0 if text1 == text2 else 0.0
    
    def _aggregate_similarities(self, similarities: List[float]) -> float:
        """Aggregate individual argument similarities"""
        if not similarities:
            return 1.0
        
        similarities_array = np.array(similarities)
        
        if self.aggregation_method == "mean":
            return float(np.mean(similarities_array))
        elif self.aggregation_method == "weighted_mean":
            # Give more weight to higher similarities
            weights = similarities_array
            if np.sum(weights) == 0:
                return 0.0
            return float(np.average(similarities_array, weights=weights))
        elif self.aggregation_method == "min":
            return float(np.min(similarities_array))
        elif self.aggregation_method == "max":
            return float(np.max(similarities_array))
        else:
            return float(np.mean(similarities_array))


class ToolCallsAccuracy(Metric):
    distance: ToolCallDistance = Field(ExactMatchToolCallDistance())
    threshold: float = Field(0.5)
    include_reason: bool = Field(True)
    strict_mode: bool = Field(True)
    

    @abstractmethod
    def measure(
        self,
        input: AssistantInput,
        expected: AssistantOutput,
        actual: AssistantOutput
    ) -> EvaluationResult:
        try:
            expected_tool_calls = expected.tools_called
            actual_tool_calls = actual.tools_called
            
            if len(expected_tool_calls) == 0 and len(actual_tool_calls) == 0:
                return EvaluationResult(
                    score=1.0,
                    verdict=EvaluationVerdict.PASSED,
                    reason='No tools expected or called - perfect match'
                )
            
            if len(expected_tool_calls) != len(actual_tool_calls) and self.strict_mode:
                if self.strict_mode:
                    return EvaluationVerdict(
                        score=0.0,
                        verdict=EvaluationVerdict.FAILED,
                        reason=f'Tool count mismatch: expected {len(expected_tool_calls)}, got {len(actual_tool_calls)}'
                    )
            
            similarities = []
            for expected_tool in expected_tool_calls:
                row_similarities = []
                for actual_tool in actual_tool_calls:
                    similarity = self.distance.measure(expected_tool, actual_tool)
                    row_similarities.append(similarity)
                similarities.append(row_similarities)
            
            # Use greedy matching algorithm
            total_simiarity = 0.0
            used_actual_indices = set()
            
            for i, expected_tool in enumerate(expected_tool_calls):
                best_similarity = 0.0
                best_j = -1
                
                for j, actual_tool in enumerate(actual_tool_calls):
                    if j in used_actual_indices:
                        continue # aready matched
                    
                    similarity = similarities[i][j] # expected i to actual j
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_j = j
                
                # -1 if already matched all actual calls (non-strict mode)
                if best_j != -1:
                    used_actual_indices.add(best_j)
                    total_simiarity += best_similarity
            
            score = total_simiarity / max(len(expected_tool_calls), len(actual_tool_calls))
            return EvaluationResult(
                score=score,
                verdict=EvaluationVerdict.PASSED if score >= self.threshold else EvaluationVerdict.FAILED,
                reason=f'Tool calls similarity score: {self.score:.3f}\nExpected: {[f"{t.name}({t.input_parameters})" for t in expected_tool_calls]}\nActual: {[f"{t.name}({t.input_parameters})" for t in actual_tool_calls]}'
            )
        except Exception as e:
            return EvaluationVerdict(
                score=0.0,
                verdict=EvaluationVerdict.ERROR,
                reason=f'Error during evaluation: {str(e)}'
            )
