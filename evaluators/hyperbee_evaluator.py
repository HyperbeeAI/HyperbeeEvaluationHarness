from enum import Enum
from helm_evaluator import HelmEvaluator
from lm_eval_harness_evaluator import LMEvalHarnessEvaluator
from mtbench_evaluator import MTBenchEvaluator
from flask_evaluator import FlaskEvaluator
class Evaluators(Enum):
    HELM = "helm"
    LM_EVAL_HARNESS = "lm_eval_harness"
    MTBENCH = "mtbench"

class HyberbeeEvaluator:
    def __init__(self):
        self.helm_evaluator = HelmEvaluator()
        self.harness_evaluator = LMEvalHarnessEvaluator()
        self.mtbench_evaluator = MTBenchEvaluator()
        self.flask_evaluator = FlaskEvaluator()
    
    def evaluate(self, model_names, evaluator_benchmark_pairs, kwargs_helm=None, kwargs_lm_eval_harness=None, kwargs_mt_bench=None):
        results = {}
        
        helm_benchmarks = []
        lm_eval_harness_benchmarks = []
        mtbench_benchmarks = []
        flask_benchmarks = []
        for pair in evaluator_benchmark_pairs:
            try:
                if 'mt-bench' in pair:
                    mtbench_benchmarks.append(benchmark_name)
                if 'flask' in pair:
                    flask_benchmarks.append(benchmark_name)
                else:
                    evaluator_name, benchmark_name = pair.split('/')
                    if evaluator_name == Evaluators.HELM.value:
                        helm_benchmarks.append(benchmark_name)
                    elif evaluator_name == Evaluators.LM_EVAL_HARNESS.value:
                        lm_eval_harness_benchmarks.append(benchmark_name)
                    else:
                        raise ValueError(f"Invalid evaluator specified: {evaluator_name}")
            except ValueError:
                raise ValueError(f"Invalid format: {pair}. Expected format: <evaluator>/<benchmark_name>")

        # Evaluate benchmarks for each evaluator
        if helm_benchmarks:
            results['HELM'] = self.helm_evaluator.evaluate(model_names, helm_benchmarks, kwargs_helm)
        if lm_eval_harness_benchmarks:
            results['LM_EVAL_HARNESS'] = self.harness_evaluator.evaluate(model_names, lm_eval_harness_benchmarks, kwargs_lm_eval_harness)
        if mtbench_benchmarks:
            results['MTBENCH'] = self.mtbench_evaluator.evaluate(model_names, kwargs_mt_bench)
        if flask_benchmarks:
            results['FLASK'] = self.flask_evaluator.evaluate(model_names, kwargs_mt_bench)

        return results
            


