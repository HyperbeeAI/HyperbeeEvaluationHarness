import subprocess
import glob
import json


class HelmEvaluator:
    def evaluate(self, model_names, benchmark_name, max_eval_instances=1000, number_of_threads=2):
        run_entries_str = self.create_run_entries(model_names, benchmark_name)
        results  = {}

        for model_name in model_names:
            try:
                suite_name =  f"suite_{model_name}_{benchmark_name}"
                suite_folder =  f"helm/benchmark_output/runs/{suite_name}"
        
                result = subprocess.run(
                    ["helm-run", "--run-entries", run_entries_str, "--suite", suite_name, "--max-eval-instances",max_eval_instances, "-n",number_of_threads],
                    capture_output=True,
                    text=True,
                    check=True
                )
                for run_folder in glob.glob(f"{suite_folder}/*:*"):
                    if benchmark_name in run_folder:
                        results[model_name] = self.get_results_from_run_folder(run_folder)

            except subprocess.CalledProcessError as e:
                print(f"Helm evaluation failed for {model_name}. (helm-run)")

            
        return results

    def create_run_entries(self, model_names, benchmark_name):
        run_entries =[]
        for model_name in model_names:
            run_entries.append(f"{benchmark_name}:model={model_name}")
        return " ".join(run_entries).strip()
        
    def get_results_from_run_folder(self, run_folder):
        results = {}
        run_spec_file = run_folder + "/run_spec.json"
        stats_file = run_folder + "/stats.json"

        with open(run_spec_file, 'r') as f:
            run_spec = json.loads(f.read())
                
        metrics = []
        for metric_class in run_spec['metric_specs']:
            try:
                for metric in metric_class['args']['names']:
                    metrics.append(metric)
            except:
                pass
        
        with open(stats_file, 'r') as f:
            stats = json.loads(f.read())
        
        for stat in stats:
            if stat['name']['name'] in metrics and stat['name']['split'] == 'test':
                results[stat['name']['name']] = stat['mean']
        return results