#!/user/bin/env python
# coding: utf-8

import os, sys, subprocess, re, requests

UNIT_PATH = "/home/cchilders/projects/advantage/unit_tests"

KERNEL_RELATIVE = "kernel/data"

def call_sp(command, **arg_list):
    p = subprocess.Popen(command, shell=True, **arg_list)
    p.communicate()
    
    
old_kernel_path = os.path.join(UNIT_PATH, KERNEL_RELATIVE, 'migration')
new_kernel_path = os.path.join(UNIT_PATH, KERNEL_RELATIVE, 'migration_renamed')
kernel_init     = os.path.join(new_kernel_path, '__init__.py')

old_central_path = os.path.join(UNIT_PATH, 'central', 'migration')
new_central_path = os.path.join(UNIT_PATH, 'central', 'migration_renamed')
central_init     = os.path.join(new_central_path, '__init__.py')
models_filepath  = os.path.join(new_central_path, 'models.py')
new_models_filepath  = os.path.join(old_central_path, 'models.py')

call_sp('mv {} {}'.format(old_kernel_path, new_kernel_path))
call_sp('mkdir {}'.format(old_kernel_path))
call_sp('touch {}'.format(kernel_init))

call_sp('mv {} {}'.format(old_central_path, new_kernel_path))
call_sp('mkdir {}'.format(old_central_path))
call_sp('touch {}'.format(central_init))
call_sp('cp {} {}'.format(models_filepath, new_models_filepath))