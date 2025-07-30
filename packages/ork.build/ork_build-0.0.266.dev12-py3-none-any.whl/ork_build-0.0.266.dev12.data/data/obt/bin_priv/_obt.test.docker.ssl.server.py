#!/usr/bin/env python3

from obt import path, command, docker

command.run(["obt.docker.build.py","ssltest"])
command.run(["obt.docker.launch.py","ssltest"])

 
