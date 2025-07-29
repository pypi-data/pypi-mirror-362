# CTAO Workload Management System

The first time you want to run the local cluster:
`git submodule update --init --recursive`

To start a `Kind` local cluster, deploy the chart in it, and run the test, do:

```bash
make
```

## Charts

## Docker images

Docker images are stored on the CTAO Harbor registry, for [wms-server](https://harbor.cta-observatory.org/harbor/projects/4/repositories/wms-server/artifacts-tab), [wms-client](https://harbor.cta-observatory.org/harbor/projects/4/repositories/wms-client/artifacts-tab) and [wms-ce](https://harbor.cta-observatory.org/harbor/projects/4/repositories/wms-ce/artifacts-tab).

## Test Report

The WMS test report can be retrieve from the CI pipeline artifact.
