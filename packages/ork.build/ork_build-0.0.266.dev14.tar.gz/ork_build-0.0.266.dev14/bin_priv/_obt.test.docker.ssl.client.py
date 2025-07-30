#!/usr/bin/env python3

from obt import path, command, docker 
ssltest_dir = docker.dir_of_module("ssltest")
ssltest = docker.descriptor("ssltest")
print(ssltest)
cmd_to_run = ssltest_dir/"examples"/"test-zmq-ping-multi.py"
print(cmd_to_run)
assert(False)
command.run([cmd_to_run], do_log=True)

 
