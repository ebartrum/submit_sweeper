#!/usr/bin/env python

import submitit
import os
import argparse
import itertools

def get_command_list(input):
    words = input.split(" ")
    shared_command = ' '.join(filter(lambda w: '=' not in w, words))
    sweep_dict = {}
    for word in words:
        if '=' in word:
            assert len(word.split('=')) == 2
            arg_name = word.split('=')[0]
            value_list = word.split('=')[1].split(',')
            sweep_dict[arg_name] = value_list
    arg_assignment_sweep_list = []
    for k,v in sweep_dict.items():
        arg_assignment_sweep_list.append([f"{k}={val}" for val in v])

    command_list = []
    for element in itertools.product(*arg_assignment_sweep_list):
        command_list.append(shared_command + " " + " ".join(element))
    return command_list

parser = argparse.ArgumentParser()
parser.add_argument("command", type=str)
parser.add_argument("-d", "--dev", help="dev run", action="store_true")
args = parser.parse_args()
if args.dev:
    partition="devel"
    time=60
else:
    partition="small"
    time=60*24*3

command_list = get_command_list(args.command)
print(f"Submitting job array with following {len(command_list)} expts")
for com in command_list:
    print(com)
print("-------------------------------------------")

executor = submitit.AutoExecutor(folder="logs")
executor.update_parameters(timeout_min=time, slurm_partition=partition,
        slurm_gres="gpu:1")

jobs = []
with executor.batch():
    for command in command_list:
        job = executor.submit(os.system, command)
        jobs.append(job)

outputs = [job.result() for job in jobs]
full_stderr = job.stderr()
