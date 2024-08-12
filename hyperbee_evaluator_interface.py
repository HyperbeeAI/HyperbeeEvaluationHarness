from enum import Enum
from evaluators.helm_evaluator import HelmEvaluator
from evaluators.lm_eval_harness_evaluator import LMEvalHarnessEvaluator
from evaluators.mtbench_evaluator import MTBenchEvaluator
from evaluators.flask_evaluator import FlaskEvaluator
import argparse
import json
class Evaluators(Enum):
    HELM = "helm"
    LM_EVAL_HARNESS = "lm_eval_harness"
    MTBENCH = "mtbench"
    FLASK = "flask"

class HyperbeeEvaluator:
    def __init__(self):
        self.helm_evaluator = HelmEvaluator()
        self.harness_evaluator = LMEvalHarnessEvaluator()
        self.mtbench_evaluator = MTBenchEvaluator()
        self.flask_evaluator = FlaskEvaluator()
    
    def evaluate(self, model_names, tasks, kwargs_helm=None, kwargs_lm_eval_harness=None, kwargs_mt_bench=None):
        results = {}
        
        helm_benchmarks = []
        lm_eval_harness_benchmarks = []
        mtbench_benchmarks = []
        flask_benchmarks = []
        for pair in tasks:
            try:
                if 'mt-bench' in pair:
                    mtbench_benchmarks.append("mt-bench")
                elif 'flask' in pair:
                    flask_benchmarks.append("flask")
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
            try:
                results['HELM'] = self.helm_evaluator.evaluate(model_names, helm_benchmarks)
            except:
                print("Problem Occured during helm evaluation.")
                results['HELM'] = "ERROR"
        if lm_eval_harness_benchmarks:
            try:
                results['LM_EVAL_HARNESS'] = self.harness_evaluator.evaluate(model_names, lm_eval_harness_benchmarks)
            except:
                print("Problem Occured during lm-eval-harness evaluation.")
                results['LM_EVAL_HARNESS'] = "ERROR"
        if mtbench_benchmarks:
            try:
                results['MTBENCH'] = self.mtbench_evaluator.evaluate(model_names)
            except:
                print("Problem Occured during mt-bench evaluation.")
                results['MTBENCH'] = "ERROR"
        if flask_benchmarks:
            try:
                results['FLASK'] = self.flask_evaluator.evaluate(model_names)
            except:
                print("Problem Occured during flask evaluation.")
                results['FLASK'] = "ERROR"

        return results
            

def main():
    parser = argparse.ArgumentParser(description="Evaluate models using various benchmarks.")
    parser.add_argument('--model_names', nargs='+', required=True, help="List of model names to evaluate.")
    parser.add_argument('--tasks', nargs='+', required=True, help="List of tasks.")
   
    args = parser.parse_args()

    evaluator = HyperbeeEvaluator()
    results = evaluator.evaluate(
        model_names=args.model_names,
        tasks=args.tasks,
    )
    print(json.dumps(results, indent=2))
    with open(f"results_{str(args.model_names)}_{args.tasks}.json", "w") as outfile: 
        json.dump(results, outfile,indent=2)

if __name__ == "__main__":
    main()
