#!/usr/bin/env python

import yaml
import os
import time
import sys
import subprocess
from utils import puts

filename = './config.yaml'
config = yaml.load(open(filename, 'r').read())
project_name = config['project_name']
namespace = config['namespace']
react_app_base_url = config['react_app_base_url']

env = ("--set namespace=%s --set react_app_base_url=%s" %(namespace, react_app_base_url))
puts(env)
cmd = "helm install --name=%s-frontend ./frontend %s" %(project_name, env)
puts(cmd)
os.system(cmd)