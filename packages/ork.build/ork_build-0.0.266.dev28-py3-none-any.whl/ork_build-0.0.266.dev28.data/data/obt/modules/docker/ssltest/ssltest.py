from obt import dep, path, command, docker, wget, pathtools, host
from obt.deco import Deco
import obt.module
import time, re, socket, os, sys
from pathlib import Path
deco = obt.deco.Deco()

this_path = os.path.realpath(__file__)
this_dir = Path(os.path.dirname(this_path))

###############################################################################

class dockerinfo:
  ###############################################
  def __init__(self):
    super().__init__()
    self.type = docker.Type.COMPOSITE # use docker-compose
    self._name = "ssltest"
    self._manifest_path = path.manifests_root()/self._name
  ###############################################
  # build the docker images
  ###############################################
  def build(self, build_args):
    os.system("rm -f %s" % str(self._manifest_path))
    assert(build_args != None)
    os.chdir(str(this_dir))
    print("Building ZMQ SSL example in:", this_dir)
    
    # Use OBT methodology - call bin/build.py with build_args
    chain = command.chain()
    chain.run(["pbin/build.py"] + build_args)
    OK = chain.ok()
    if OK:
      os.system("touch %s" % str(self._manifest_path))
    return OK
  ###############################################
  # kill active docker containers
  ###############################################
  def kill(self):
    os.chdir(str(this_dir))
    print("Stopping ZMQ SSL example containers...")
    command.run(["docker", "compose", "down"])
  ###############################################
  # launch docker containers
  ###############################################
  def launch(self, launch_args, environment=None, mounts=None):
    os.chdir(this_dir)
    
    print("\n" + "="*60)
    print("🚀 LAUNCHING ZMQ SSL EXAMPLE")
    print("="*60)
    print("ZMQ Server: Internal only (port 5555)")
    print("SSL Proxy: External SSL endpoint (port 8443)")
    print("Mode: FOREGROUND (Ctrl-C to stop)")
    print("="*60)
    
    # Start services in background first to let them initialize
    print("\n📦 Starting services...")
    command.run(["docker", "compose", "up"])
    
  ###############################################
  # stop the docker containers
  ###############################################
  def stop(self):
    os.chdir(str(this_dir))
    command.run(["docker", "compose", "down"])
  ###############################################
  # show logs
  ###############################################
  def logs(self, service=None):
    os.chdir(this_dir)
    if service:
      command.run(["docker", "compose", "logs", "-f", service])
    else:
      command.run(["docker", "compose", "logs", "-f"])
  ###############################################
  # information dictionary
  ###############################################
  def info(self):
    return {
      "name": "ssltest",
      "description": "Example of SSL-wrapping an unprotected ZMQ server",
      "manifest": str(self._manifest_path),
    }