#!/usr/bin/env python

import yaml
import os
import time
import sys
import subprocess
import uuid
import json
from utils import puts

filename = './config.yaml'
config = yaml.load(open(filename, 'r').read())
project_name = config['project_name']
cluster_name = config['Cluster']['cluster_name']
domain = config['domain']
namespace = config['namespace']

env = ("--set namespace=%s --set cluster_name=%s --set domain=%s" %(namespace, cluster_name, domain))
puts(env)

os.system("kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/rbac-role.yaml")

#create policy
extract_arn = None
policies = os.popen("aws iam list-policies | jq '.Policies'").read().strip()
policies = json.loads(policies)
for policy in policies:
    if policy['PolicyName'] == "ALBIngressControllerIAMPolicy":
        extract_arn = policy['Arn']

if extract_arn == None:
    create_policy = "aws iam create-policy --policy-name ALBIngressControllerIAMPolicy --policy-document file://scripts/iam-policy.json | jq -r '.Policy.Arn'"
    print create_policy
    extract_arn = os.popen(create_policy).read().strip()


create_oidc_prov = "eksctl utils associate-iam-oidc-provider --cluster=%s --approve"%(cluster_name)
print create_oidc_prov
os.system(create_oidc_prov)

create_sa = '''
eksctl create iamserviceaccount \
       --cluster=%s \
       --namespace=kube-system \
       --name=alb-ingress-controller \
       --attach-policy-arn=%s \
       --override-existing-serviceaccounts \
       --approve \
''' %(cluster_name, extract_arn)

print create_sa
os.system(create_sa)

os.system("kubectl apply -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.6/deploy/manifests/00-crds.yaml")

os.system("kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.14.1/cert-manager.crds.yaml")

apply_ingress = "helm install --name=%s-ingress ./ingress %s" %(project_name, env)
puts(apply_ingress)
os.system(apply_ingress)
