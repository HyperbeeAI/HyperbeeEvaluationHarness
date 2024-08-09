source hyperbee-eval-venv/bin/activate
cd lm-evaluation-harness
pip install -e .

cd ..
cp -rf my_lm-evaluation-harness/* lm-evaluation-harness/