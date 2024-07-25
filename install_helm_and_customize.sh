#install helm on a virtualenv
cd helm
python3 -m pip install virtualenv
python3 -m virtualenv -p python3.8 helm-venv
source helm-venv/bin/activate
pip install crfm-helm

cd ..
cp -r my_helm/ helm/
