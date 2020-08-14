# Pangeo Batch

The Pangeo ML working group recently discussed submitting "batch" jobs. I
unfortunately missed the meeting, but this post describes what can be done
today with a bit of work, and the many many shortcomings. The goal is to
identify what could be improved with a bit of work.

## What is Pangeo?

From a certain point of view, Pangeo is "just" JupyterHub + Dask. And if we
want a batch workflow, we don't need JupyterHub's single-user stuff, ergo Pangeo
Batch is "just" Dask? Not quite, but of the pieces Pangeo has today, we just
want access to the scalable compute. Thanks to Dask-Gateway, we can do that.

Pangeo's Dask Gateways are deployed with JupyterHub auth. JupyterHub allows
creating secret tokens to impersonate yourself from outside the Hub. We'll
get a token and export it in our *local* shell as `PANGEO_TOKEN`.

## Connecting from outside the cluster

With the `PANGEO_TOKEN`, we can connect to Dask Gateway by explicitly providing
a few things that are normally set for us when we're using the hub.

```python
import os

from dask_gateway import Gateway
from dask_gateway.auth import JupyterHubAuth

# Explicit auth, since we aren't in the Hub
auth = JupyterHubAuth(os.environ["PANGEO_TOKEN"])

gateway = Gateway(
    # Explicit address, since we aren't in the Hub
    address="https://us-central1-b.gcp.pangeo.io/services/dask-gateway/",
    auth=auth
)
gateway.list_clusters()
```

## Batch jobs

We're basically there.

## What's missing?

Probably many thinigs.

* State managament (What jobs have I submitted? What's their status? What's their output?)
