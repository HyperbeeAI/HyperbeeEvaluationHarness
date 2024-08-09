#install helm on a virtualenv
source hyperbee-eval-venv/bin/activate
pip install crfm-helm[all]
cp -rf my_helm/* helm/
