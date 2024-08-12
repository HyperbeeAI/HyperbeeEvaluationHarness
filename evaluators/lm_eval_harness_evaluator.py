import glob
import os
from common_methods import run_command_and_print
class LMEvalHarnessEvaluator:
    def evaluate(self, model_names, benchmark_names, **kwargs):
        results  = {}
        os.chdir("lm-evaluation-harness")
        for model_name in model_names:
            try:
                # Base command
                command = ["python", "-m", "lm_eval"]

                # Check model type and construct model arguments
                if "openai" in model_name:
                    model_provider = "openai-chat-completions"
                    model_args = f"model={model_name.split('/')[-1]}"
                elif "anthropic" in model_name:
                    model_provider = "anthropic-chat-completions"
                    model_args = f"model={model_name.split('/')[-1]}"
                else:
                    model_provider = "hf"
                    model_args = f"pretrained={model_name}"
                
                command.extend(["--model", model_provider])
                command.extend(["--model_args", model_args])
                command.extend(["--tasks", ",".join(benchmark_names)])
                if "openai" in model_name or "anthropic" in model_name:
                    command.extend(["--apply_chat_template"])
                # Add other keyword arguments
                
                if kwargs:
                    for key, value in kwargs.items():
                        command.extend([f"--{key.replace('_', '-')}", str(value)])
                    
                result = run_command_and_print(command)
                result = result.split("gen_kwargs:")[-1]
                results[model_name] = result[result.find("Tasks"):]
            except:
                print(f"lm-eval-harness evaluation failed for {model_name}.")
                results[model_name] = "ERRORs"
        os.chdir("..")
        return results