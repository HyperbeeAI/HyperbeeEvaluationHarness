# Hyberbee Evaluation Repo
## Quick Start
**Installation**
```
git clone --recurse-submodules https://github.com/HyperbeeAI/HyperbeeEvaluationHarness.git
cd HyperbeeEvaluationHarness
bash install_all_modules.sh
```
**Activate the environment and set api variables**
```
source hyperbee-eval-venv/bin/activate
export OPENAI_API_KEY=sk********x
```

**Run Evals by specifying models and benchmarks. tasks:(mt-bench, flask, helm/*, lm_eval_harness/*) models(provider/model_name)** * *Note:Huggingface models wont generate results for helm benchmarks. Similarly lm-eval-harness repositry won't generate results for some APIs like gemini's vertexAPI. To see supported models and providers check the original repos' readmes* *
```
python hyperbee_evaluator_interface.py --model_names facebook/opt-1.3b openai/gpt-3.5-turbo-0125 --tasks lm_eval_harness/mmlu_anatomy_generative mt-bench helm/gsm
```

