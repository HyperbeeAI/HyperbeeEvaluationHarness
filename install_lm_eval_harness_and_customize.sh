source hyperbee-eval-venv/bin/activate
cd lm-evaluation-harness
pip install -e .

cd ..
cp -rf my_lm-evaluation-harness/* lm-evaluation-harness/

python hyberbee_evaluator.py --model_names openai/gpt-3.5-turbo --evaluator_benchmark_pairs helm/gsm8k
