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

env = ("--set namespace=%s" %(namespace))
puts(env)
cmd = "helm install --name=%s-backend ./backend %s" %(project_name, env)
puts(cmd)
os.system(cmd)