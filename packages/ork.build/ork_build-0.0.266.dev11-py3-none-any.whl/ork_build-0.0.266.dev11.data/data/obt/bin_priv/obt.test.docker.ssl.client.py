#!/usr/bin/env python3

from obt import path, command, docker 
ssltest = docker.dir_of_module("ssltest")
command.run([ssltest/"examples"/"test-zmq-ping-multi.py"], do_log=True)

 
