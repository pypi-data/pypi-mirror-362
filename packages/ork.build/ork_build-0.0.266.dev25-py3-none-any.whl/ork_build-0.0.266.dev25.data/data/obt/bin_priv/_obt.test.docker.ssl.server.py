#!/usr/bin/env python3

from obt import path, command, docker

module = docker.descriptor("ssltest")
module.build([])
module.launch()
try:
  while True:
    time.sleep(1)
except KeyboardInterrupt:
  module.stop()
  exit(0)

 
