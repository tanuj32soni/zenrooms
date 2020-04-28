# Zenrooms

## Prerequisites

Tools and packages required for deployment scripts:
- [Python](https://www.python.org/downloads/) (packages: [pyyaml](https://pypi.org/project/PyYAML/))
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [jq](https://stedolan.github.io/jq/download/)
- [helm(version:2)](https://v2.helm.sh/docs/using_helm/#from-script)
- aws cli and eksctl ([link to install aws cli and eksctl](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html))
- [Configure aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html). While configuring aws cli using 'aws configure' command as mentioned in the above document, Give 'Default region name' same as that of the project region and 'Default output format' as 'json'. 


## Explanation
There are three helm charts each for backend, frontend and ingress respectively. By installing these charts, correspoding resorces will be created.

Helm charts are created for each of the components to maintain modularity and easy for undestanding.


### SSL provisioning
Here, certmanager is used to manage the lifecycle of certificates. cert manager is a kubernetes certificates management controller which helps with issuing certificates from different issuers and ensures that certificates are up to date and valid and attempts to renew the certificates at a configured time before expiry.

By adding custom resource definition of cert manager to kubernetes, we can create resources such as `Issuer` and `Certificate`. By creating these resources in kubernetes, cert manager controller will handle the issuing certificates and storing the certificates.

Here, lets encrypt is used as certificate issuer. letsencrypt is a free, automated and open certificate authority. The certificates issued by letsencrypt are browser trusted.

In issuer resource, letsencrypt is refernced as certificate authority. By creating `Issuer` and `Certificate` resources, cert manager will register with the letsencrypt acme server and handles the http01 challenge to prove that we own the domain that we have used and gets the certificate from the lectsencypt CA. After getting the certificate from the CA, cert manager will store the key and certificate as a secret.

## Bonus points achieved
- Application is available via SSL 
- Automate the cluster setup
- Application is auto-scaling.

## Setup

Update the `config.yaml` file as mentioned below.
```
Cluster:
  region: us-east-1        ## Region in which cluster will be deplyed
  cluster_name: staging    ## Cluster name

project_name: zenrooms     ## A unique name
namespace: zenrooms-app    ## name of the namespace to deploy the application.
domain: devapp.ecourts.ml  ## domain of the application
react_app_base_url: https://devapp.ecourts.ml/api/  ## Base url
``` 

If the applicaion needs to be deployed in different environments, update the `config.yaml` accordingly and run the scripts.

To setup the application, follow the below commands. Run the following commands from project root directory.

### Deploy cluster

```
python scripts/00-setup_cluster.py
```

### Deploy Backend
```
python scripts/01-create_backend.py
```

### Deploy Frontend
```
python scripts/02-create_frontend.py
```

### Deploy ingress
```
python scripts/03-create_ingress.py
```

### URL of deployed cluster

```
https://devapp.ecourts.ml/
```