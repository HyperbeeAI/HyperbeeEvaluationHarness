#install helm on a virtualenv
source hyperbee-eval-venv/bin/activate
cd helm
pip install crfm-helm

cd ..
cp -rf my_helm/* helm/
