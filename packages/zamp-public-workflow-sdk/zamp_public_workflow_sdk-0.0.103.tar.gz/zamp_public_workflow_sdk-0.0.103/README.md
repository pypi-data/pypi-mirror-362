# public-workflow-sdk

# Steps to build
rm -rf dist/ build/ *.egg-info
python -m build
python -m twine upload dist/*


gcloud storage cp memray-flamegraph-workers.py.1.html gs://zamp_data_metrics/
