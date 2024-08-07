import subprocess
import glob
import json
import os

class HelmEvaluator:
    def evaluate(self, model_names, benchmark_names, max_eval_instances=10, number_of_threads=2, **kwargs):
        os.chdir("helm")
        results  = {}

        for model_name in model_names:
            for benchmark_name in benchmark_names:
                result = ""
                try:
                    run_entries_str = f"{benchmark_name}:model={model_name}"
                    suite_name =  f"suite_{model_name}_{benchmark_name}"
                    suite_folder =  f"benchmark_output/runs/{suite_name}"
            
                    # Start building the command
                    command = ["helm-run", "--run-entries", run_entries_str, "--suite", suite_name, "--max-eval-instances", str(max_eval_instances), "-n", str(number_of_threads)]
                    
                    # Add additional kwargs to the command
                    if kwargs:
                        for key, value in kwargs.items():
                            command.append(f"--{key.replace('_', '-')}")
                            if isinstance(value, bool):
                                if value:
                                    command.append('true')
                                else:
                                    command.append('false')
                            else:
                                command.append(str(value))
                    
                    result = subprocess.run(
                        command,
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    for run_folder in glob.glob(f"{suite_folder}/*:*"):
                        if benchmark_name in run_folder:
                            results[suite_name] = self.get_results_from_run_folder(run_folder)

                except subprocess.CalledProcessError as e:
                    print(f"Helm evaluation failed for {model_name}. (helm-run)")
                    print(f"Command: {e.cmd}")
                    print(f"Return Code: {e.returncode}")
                    print(f"Standard Output: {e.stdout}")
                    print(f"Standard Error: {e.stderr}")
                       
        return results
    
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