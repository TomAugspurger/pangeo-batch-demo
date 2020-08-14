import os

import gcsfs
from dask_gateway import Gateway
from dask_gateway.auth import JupyterHubAuth
from distributed import fire_and_forget, wait
from sklearn.datasets import make_classification
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import joblib


def main():
    # Fit a scikit-learn grid search, using Dask, and persist to pangeo-scratch
    # bucket.
    X, y = make_classification(n_samples=1000, random_state=0)
    param_grid = {"C": [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
                  "kernel": ['rbf', 'poly', 'sigmoid'],
                  "shrinking": [True, False]}

    grid_search = GridSearchCV(SVC(gamma='auto', random_state=0),
                               param_grid=param_grid,
                               return_train_score=False,
                               cv=5,
                               n_jobs=-1)

    with joblib.parallel_backend('dask'):
        grid_search.fit(X, y)

    fs = gcsfs.GCSFileSystem()
    path = "gcs://pangeo-scratch/tomaugspurger/model-1.pkl"
    with fs.open(path, "wb") as f:
        joblib.dump(grid_search, f)
    return path


if __name__ == "__main__":
    auth = JupyterHubAuth(os.environ["PANGEO_TOKEN"])
    # Proxy address will be made easier to find.
    print("Connecting to Gateway")
    gateway = Gateway(
        address="https://staging.us-central1-b.gcp.pangeo.io/services/dask-gateway/",
        proxy_address="tls://104.197.142.28:8786",
        auth=auth
    )
    cluster = gateway.new_cluster(shutdown_on_close=False)
    client = cluster.get_client()
    print("Dashboard:", client.dashboard_link)

    cluster.scale(4)
    client.wait_for_workers(4)
    print("Cluster ready")

    fut = client.submit(main)
    fire_and_forget(fut)
