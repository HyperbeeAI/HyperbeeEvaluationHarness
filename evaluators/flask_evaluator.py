import pickle
import time
import os
import json
import subprocess
from evaluators.lm_eval_harness_evaluator import LMEvalHarnessEvaluator
import pandas as pd
from common_methods import run_command_and_print
import traceback
class FlaskEvaluator:
    def evaluate(self, model_names, **kwargs):
        results  = {}
        harness_evaluator = LMEvalHarnessEvaluator()

        for model in model_names:
            try:
                harness_evaluator.evaluate(model_names=[model], benchmark_names=["flask"])
                _ = self.generate_reviews()

                results[model] = self.aggregate_results()
            except:
                print(f"Error on flask_{model}")
                traceback.print_exc()
                results[model] = "ERROR"
        return results
    
    def generate_reviews(self, flask_results_fname="lm-evaluation-harness/flask_results.pickle"):
        try:
            with open(flask_results_fname, 'rb') as handle:
                    flask_results = pickle.load(handle)
        except:
            raise Exception(f"{flask_results_fname} was not found.")
        
        os.chdir("my_flask-eval")
        
        for qid in range(1,1741):
            answer = flask_results[str(qid)]
            ans_json = {
                    "question_id": qid,
                    "text": answer
            }
            with open(os.path.expanduser("model0.jsonl"), "a") as fout:
                fout.write(json.dumps(ans_json) + "\n")


        # Define the arguments to pass to the script
        args = [
            "gpt_review/gpt4_eval.py",
            "--key-file", "api_info.json",
            "--question-file", "flask_evaluation.jsonl",
            "--skillset-file", "skillset_description.json",
            "--answer-file", "model0.jsonl",
            "--prompt-file", "gpt_review/src/prompt.jsonl",
            "--reviewer-file", "gpt_review/src/reviewer.jsonl",
            "--output-review-file", "review.jsonl",
            "--output-error-file", "error.jsonl",
            "--max-tokens", "1024"
        ]

        # Use subprocess to run the script with the specified arguments
        result = run_command_and_print(["python"] + args)
        os.chdir("..")
        return result
    
    def aggregate_results(self, reviews_fname="my_flask-eval/review.jsonl"):
        _ = run_command_and_print(["python", "my_flask-eval/gpt_review/aggregate_difficulty_skill.py", "-m", reviews_fname])
        _ = run_command_and_print(["python", "my_flask-eval/gpt_review/aggregate_domain.py", "-m", reviews_fname])
        _ = run_command_and_print(["python", "my_flask-eval/gpt_review/aggregate_skill.py", "-m", reviews_fname])

        ds_df = pd.read_csv("my_flask-eval/review_difficulty_skill.csv")
        d_df = pd.read_csv("my_flask-eval/review_domain.csv")
        s_df = pd.read_csv("my_flask-eval/review_skill.csv")

        results={}
        results['domain_aggregated'] = d_df.to_string()
        results['skill_aggregated'] = s_df.to_string()
        results['difficulty_skill_aggregated'] = ds_df.to_string()
        return results