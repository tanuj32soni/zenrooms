# !/usr/bin/env python

import yaml
import os
import time
import sys
import subprocess
from utils import puts

filename = './config.yaml'

config = yaml.load(open(filename, 'r').read())
aws_region = config['Cluster']['region']
aws_cluster_name = config['Cluster']['cluster_name']
namespace = config['namespace']

create_cluster_command = '''
eksctl create cluster \
  --name %s \
  --region %s \
  --nodegroup-name standard-workers \
  --node-type t2.medium \
  --nodes 1 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed \
''' %(aws_cluster_name, aws_region)

print 'Executing: %s' %(create_cluster_command)
os.system(create_cluster_command)

print 'Executing: %s' %('helm init')
os.system('helm init')

print 'Executing: %s' %('kubectl create serviceaccount --namespace kube-system tiller')
os.system('kubectl create serviceaccount --namespace kube-system tiller')

create_cluster_role_binding_command = '''
kubectl create clusterrolebinding tiller-cluster-rule \
  --clusterrole=cluster-admin \
  --serviceaccount=kube-system:tiller \
'''

print 'Executing: %s' %(create_cluster_role_binding_command)
os.system(create_cluster_role_binding_command)

print 'Executing: %s' %('helm init --service-account tiller --upgrade')
os.system('helm init --service-account tiller --upgrade')

create_namespace = "kubectl create namespace %s" %(namespace)
puts(create_namespace)
os.system(create_namespace)

print 'Done!'