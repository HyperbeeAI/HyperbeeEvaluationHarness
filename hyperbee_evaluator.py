from enum import Enum
from helm_evaluator import HelmEvaluator
class Evaluators(Enum):
    HELM = "helm"
    LM_EVAL_HARNESS = "lm_eval_harness"
    MTBENCH = "mtbench"

class LmEvalHarnessEvaluator:
    def evaluate(self, model_names, benchmark_name):
        # Placeholder for actual evaluation logic
        return ["result1"]

class MTBenchEvaluator:
    def evaluate(self, model_names, benchmark_name):
        # Placeholder for actual evaluation logic
        return ["result2"]
class HyberbeeEvaluator:
    def __init__(self):
        self.helm_evaluator = HelmEvaluator()
        self.harness_evaluator = LmEvalHarnessEvaluator()
        self.mtbench_evaluator = MTBenchEvaluator()
    
    def evaluate(self, model_names, evaluator_benchmark_pairs):
        results = {}
        
        for pair in evaluator_benchmark_pairs:
            try:
                evaluator_name, benchmark_name = pair.split('/')
                evaluator = self._get_evaluator(evaluator_name)
                results[pair] = evaluator.evaluate(model_names, benchmark_name)
            except ValueError:
                raise ValueError(f"Invalid format: {pair}. Expected format: <evaluator>/<benchmark_name>")
            except KeyError:
                raise ValueError(f"Invalid evaluator specified: {evaluator_name}")
        
        return results
    
    def _get_evaluator(self, evaluator_name):
        if evaluator_name == Evaluators.HELM.value:
            return self.helm_evaluator
        elif evaluator_name == Evaluators.LM_EVAL_HARNESS.value:
            return self.harness_evaluator
        elif evaluator_name == Evaluators.MTBENCH.value:
            return self.mtbench_evaluator
        else:
            raise KeyError(evaluator_name)


