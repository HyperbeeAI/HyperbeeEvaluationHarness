import pickle
import time
import os
import json
import subprocess
from lm_eval_harness_evaluator import LMEvalHarnessEvaluator
import pandas as pd

class FlaskEvaluator:
    def evaluate(self, model_names, **kwargs):
        results  = {}
        harness_evaluator = LMEvalHarnessEvaluator()

        for model in model_names:
            harness_evaluator.evaluate(model_names=[model], benchmark_names=["flask"])
            _ = self.generate_reviews()

            results[model] = self.aggregate_results()
        return results
    
    def generate_reviews(self, flask_results_fname="lm-evaluation-harness/flask_results.pickle"):
        try:
            with open(flask_results_fname, 'rb') as handle:
                    flask_results = pickle.load(handle)
        except:
            raise Exception(f"{flask_results_fname} was not found.")
        
        
        for qid in range(1,1741):
            answer = flask_results[qid]
            ans_json = {
                    "question_id": qid,
                    "text": answer
            }
            with open(os.path.expanduser("my_flask-eval/model0.jsonl"), "a") as fout:
                fout.write(json.dumps(ans_json) + "\n")


        # Define the arguments to pass to the script
        args = [
            "my_flask-eval/gpt_review/gpt4_eval.py",
            "--key-file", "my_flask-eval/api_info.json",
            "--question-file", "my_flask-eval/flask_evaluation.jsonl",
            "--skillset-file", "my_flask-eval/skillset_description.json",
            "--answer-file", "my_flask-eval/model0.jsonl",
            "--prompt-file", "my_flask-eval/gpt_review/src/prompt.jsonl",
            "--reviewer-file", "my_flask-eval/gpt_review/src/reviewer.jsonl",
            "--output-review-file", "my_flask-eval/review.jsonl",
            "--output-error-file", "my_flask-eval/error.jsonl",
            "--max-tokens", "1024"
        ]

        # Use subprocess to run the script with the specified arguments
        result = subprocess.run(["python"] + args, capture_output=True, text=True)
        return result.stdout
    
    def aggregate_results(self, reviews_fname="my_flask-eval/review.jsonl"):
        _ = subprocess.run(["python", "my_flask-eval/gpt_review/aggregate_difficulty_skill.py", "-m", reviews_fname], capture_output=True, text=True)
        _ = subprocess.run(["python", "my_flask-eval/gpt_review/aggregate_domain.py", "-m", reviews_fname], capture_output=True, text=True)
        _ = subprocess.run(["python", "my_flask-eval/gpt_review/aggregate_skill.py", "-m", reviews_fname], capture_output=True, text=True)

        ds_df = pd.read_csv("my_flask-eval/review_difficulty_skill.csv")
        d_df = pd.read_csv("my_flask-eval/review_domain.csv")
        s_df = pd.read_csv("my_flask-eval/review_skill.csv")

        results={}
        results['domain_aggregated'] = d_df.to_string()
        results['skill_aggregated'] = s_df.to_string()
        results['difficulty_skill_aggregated'] = ds_df.to_string()
        return results