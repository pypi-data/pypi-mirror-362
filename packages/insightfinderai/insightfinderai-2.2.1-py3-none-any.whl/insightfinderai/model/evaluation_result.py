"""
EvaluationResult model for the InsightFinder AI SDK.
"""
from typing import List, Optional, Union, Dict, Any


class EvaluationResult:
    """Represents an evaluation result with formatted display and object access."""
    
    def __init__(self, evaluation_data: dict, trace_id: Optional[str] = None, prompt: Optional[str] = None, response: Optional[str] = None):
        self.evaluations = evaluation_data.get('evaluations', [])
        self.trace_id = trace_id or evaluation_data.get('traceId', '')
        self.prompt = prompt
        self.response = response
        self.is_passed = not self.evaluations  # True if no evaluations (empty list = passed)
        self.summary = self._generate_summary()
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics for evaluations."""
        # For single evaluation, total prompts is always 1
        total_prompts = 1
        
        # If no evaluations, it's a pass
        if not self.evaluations:
            return {
                'total_prompts': total_prompts,
                'passed_evaluations': 1,
                'failed_evaluations': 0,
                'top_failed_evaluation': None
            }
        
        # If evaluations exist, it's a fail (regardless of scores)
        passed_evaluations = 0
        failed_evaluations = 1
        
        # Count evaluation types for top failed evaluation
        eval_type_counts = {}
        for eval_item in self.evaluations:
            eval_type = eval_item.get('evaluationType', 'Unknown')
            eval_type_counts[eval_type] = eval_type_counts.get(eval_type, 0) + 1
        
        # Find top failed evaluation type(s)
        top_failed_evaluation = None
        if eval_type_counts:
            max_count = max(eval_type_counts.values())
            top_failed_types = [eval_type for eval_type, count in eval_type_counts.items() if count == max_count]
            top_failed_evaluation = top_failed_types if len(top_failed_types) > 1 else top_failed_types[0]
        
        return {
            'total_prompts': total_prompts,
            'passed_evaluations': passed_evaluations,
            'failed_evaluations': failed_evaluations,
            'top_failed_evaluation': top_failed_evaluation
        }
    
    def print(self) -> str:
        """Print and return evaluation results for clean display."""
        result = self.__str__()
        print(result)
        return result
    
    def __str__(self):
        """Format evaluation results for clean display."""
        result = "[Evaluation Results]\n"
        result += f"Trace ID : {self.trace_id}\n"
        result += "\n"
        
        # Always show prompt and response if available
        if self.prompt:
            result += "Prompt:\n"
            result += f">> {self.prompt}\n"
            result += "\n"
        
        if self.response:
            result += "Response:\n"
            result += f">> {self.response}\n"
            result += "\n"
        
        # Show evaluations if available
        if self.evaluations:
            result += "Evaluations:\n"
            result += "-" * 40 + "\n"
            
            for i, eval_item in enumerate(self.evaluations, 1):
                eval_type = eval_item.get('evaluationType', 'Unknown')
                score = eval_item.get('score', 0)
                explanation = eval_item.get('explanation', 'No explanation provided')
                
                result += f"{i}. Type        : {eval_type}\n"
                result += f"   Score       : {score}\n"
                result += f"   Explanation : {explanation}\n"
                if i < len(self.evaluations):
                    result += "\n"
        else:
            result += "Evaluations:\n"
            result += "-" * 40 + "\n"
            result += "PASSED"
        
        return result

    def format_for_chat(self):
        """Format evaluation results for display within chat response (no prompt/response repetition)."""
        if not self.evaluations:
            return "Evaluations:\n" + "-" * 40 + "\nPASSED"
        
        result = "Evaluations:\n"
        result += "-" * 40 + "\n"
        
        for i, eval_item in enumerate(self.evaluations, 1):
            eval_type = eval_item.get('evaluationType', 'Unknown')
            score = eval_item.get('score', 0)
            explanation = eval_item.get('explanation', 'No explanation provided')
            
            result += f"{i}. Type        : {eval_type}\n"
            result += f"   Score       : {score}\n"
            result += f"   Explanation : {explanation}\n"
            if i < len(self.evaluations):
                result += "\n"
        
        return result

