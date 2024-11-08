import pickle
import time
import os
import json
import subprocess
from evaluators.lm_eval_harness_evaluator import LMEvalHarnessEvaluator
from common_methods import run_command_and_print


class MTBenchEvaluator:
    def evaluate(self, model_names, **kwargs):
        results  = {}
        harness_evaluator = LMEvalHarnessEvaluator()

        for model in model_names:
            try:
                harness_evaluator.evaluate(model_names=[model], benchmark_names=["mt_bench_step1"])
                harness_evaluator.evaluate(model_names=[model], benchmark_names=["mt_bench_step2"])
                judgements = self.generate_judgements()
                results[model] = judgements
            except:
                 print(f"Error on mt-bench_{model}")
                 results[model] = "ERROR"
        return results
    
    def generate_judgements(self, mode="single", step_one_results_fname="lm-evaluation-harness/mt_bench_step1_results.pickle", step_two_results_fname="lm-evaluation-harness/mt_bench_step2_results.pickle"):
        try:
            with open(step_one_results_fname, 'rb') as handle:
                    step_one_results = pickle.load(handle)
        except:
            raise Exception(f"{step_one_results_fname} was not found.")
        try:
            with open(step_two_results_fname, 'rb') as handle:
                    step_two_results = pickle.load(handle)
        except:
            raise Exception(f"{step_two_results_fname} was not found.")
        
        for qid in range(81,161):
            turn_one_answer = step_one_results[qid]
            turn_two_answer = step_two_results[qid]
            ans_json = {
                    "question_id": qid,
                    "answer_id": qid,
                    "model_id": 000,
                    "choices": [turn_one_answer,turn_two_answer],
                    "tstamp": time.time(),
            }
            with open(os.path.expanduser("my_mt-bench/model_answers/model0.jsonl"), "a") as fout:
                fout.write(json.dumps(ans_json) + "\n")


        # Define the arguments to pass to the script
        args = [
            "my_mt-bench/gen_judgment.py",
            "--bench-name", "mt_bench",
            "--judge-file", "my_mt-bench/judge_prompts.jsonl",
            "--judge-model", "gpt-4",
            "--baseline-model", "gpt-3.5-turbo",
            "--mode", "single",
            "--model-list", "model0",
            "--parallel", "2"
        ]

        # Use subprocess to run the script with the specified arguments
        _ = run_command_and_print(["python"] + args)
        result = run_command_and_print(["python", "my_mt-bench/show_result.py", "--mode", mode])
        return result