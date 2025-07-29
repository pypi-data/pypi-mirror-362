# wms

![Version: 0.0.0-dev](https://img.shields.io/badge/Version-0.0.0--dev-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: dev](https://img.shields.io/badge/AppVersion-dev-informational?style=flat-square)

A Helm chart to deploy the Workload Management System of CTAO

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://harbor.cta-observatory.org/dpps | cert-generator-grid | v2.1.0 |
| oci://harbor.cta-observatory.org/dpps | cvmfs | v0.5.0 |
| oci://registry-1.docker.io/bitnamicharts | mariadb | 20.5.5 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| cert-generator-grid | object | `{"enabled":true,"generatePreHooks":true}` | Settings for the certificate generator |
| cvmfs | object | `{"enabled":true,"publish_docker_images":["harbor.cta-observatory.org/proxy_cache/library/python:3.12-slim"]}` | Configuration for the cvmfs subchart, included for testing |
| dev | object | `{"client_image_tag":null,"mount_repo":true,"run_tests":true,"sleep":false}` | Settings for local development |
| dev.client_image_tag | string | `nil` | tag of the image used to run helm tests |
| dev.mount_repo | bool | `true` | mount the repo volume to test the code as it is being developed |
| dev.run_tests | bool | `true` | run tests in the container |
| dev.sleep | bool | `false` | sleep after test to allow interactive development |
| dirac_server | object | `{"podAnnotations":{},"podLabels":{},"podSecurityContext":{},"resetDatabase":true,"securityContext":{}}` | Setting for the main DIRAC server pod |
| dirac_server.resetDatabase | bool | `true` | Recreates DIRAC database from scratch. Useful at first installation, but destructive on update: should be changed immediately after the first installation. |
| fullnameOverride | string | `""` |  |
| image | object | `{"pullPolicy":"IfNotPresent","repository_prefix":"harbor.cta-observatory.org/dpps/wms","tag":null}` | Image settings. |
| image.repository_prefix | string | `"harbor.cta-observatory.org/dpps/wms"` | Prefix of the repository, pods will use <repository_prefix>-{server,client,ce} |
| image.tag | string | `nil` | Image tag, if not set, the chart's appVersion will be used |
| imagePullSecrets | list | `[{"name":"harbor-pull-secret"}]` | Secrets needed to access image registries |
| mariadb | object | `{"auth":{"rootPassword":"dirac-db-root"},"enabled":true,"initdbScripts":{"create-user.sql":"CREATE USER IF NOT EXISTS 'Dirac'@'%' IDENTIFIED BY 'dirac-db';\n"}}` | Configuration for the bitnami mariadb subchart. Disable if DIRAC database is provided externally. |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| resources | object | `{}` |  |
| rucio.enabled | bool | `false` |  |
| service.port | int | `8080` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.automount | bool | `true` | Automatically mount a ServiceAccount's API credentials? |
| serviceAccount.create | bool | `true` | Specifies whether a service account should be created |
| serviceAccount.name | string | `""` | If not set and create is true, a name is generated using the fullname template |
| test_ce | object | `{"enabled":true,"resources":{}}` | A simple SSH compute element for testing |
| tolerations | list | `[]` |  |
| volumeMounts | list | `[]` |  |
| volumes | list | `[]` |  |

