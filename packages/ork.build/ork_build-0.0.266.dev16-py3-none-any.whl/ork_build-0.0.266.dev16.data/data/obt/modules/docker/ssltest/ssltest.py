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
    assert(build_args != None)
    os.chdir(str(this_dir))
    print("Building ZMQ SSL example in:", this_dir)
    
    # Use OBT methodology - call bin/build.py with build_args
    chain = command.chain()
    chain.run(["pbin/build.py"] + build_args)
    OK = chain.ok()
    if OK:
      os.system("touch %s" % str(manifest_path))
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
    command.run(["docker", "compose", "up", "-d"])
    
    print("✅ Services starting... waiting for initialization...")
    time.sleep(3)
    
    # Check status
    print("\n📊 Service Status:")
    command.run(["docker", "compose", "ps"])
    
    # Show some logs to verify startup
    print("\n📋 Recent logs:")
    command.run(["docker", "compose", "logs", "--tail=10"])
    
    print("\n" + "="*60)
    print("🔗 CONNECTION INFO")
    print("="*60)
    print("SSL Endpoint: localhost:8443")
    print("ZMQ Server: Internal only (zmq-server:5555)")
    print("")
    print("🧪 TESTING:")
    print("  python examples/client-direct.py  # Direct connection test")
    print("  python examples/client-ssl.py     # SSL connection test")
    print("")
    print("🔍 MONITORING:")
    print("  docker compose logs -f zmq-server  # ZMQ server logs")  
    print("  docker compose logs -f ssl-proxy   # SSL proxy logs")
    print("="*60)
    
    # Run a quick test to verify it's working
    print("\n🧪 Running connectivity test...")
    try:
      # Simple connectivity test using netcat if available
      import socket
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.settimeout(2)
      result = sock.connect_ex(('localhost', 8443))
      sock.close()
      if result == 0:
        print("✅ SSL proxy port 8443 is reachable")
      else:
        print("❌ SSL proxy port 8443 is not reachable")
    except Exception as e:
      print(f"⚠️  Could not test connectivity: {e}")
    
    print("\n" + "="*60)
    print("📺 LIVE LOGS (Ctrl-C to stop)")
    print("="*60)
    
    try:
      # Follow logs in foreground - this will run until Ctrl-C
      command.run(["docker", "compose", "logs", "-f"])
    except KeyboardInterrupt:
      print("\n\n🛑 Stopping services...")
      command.run(["docker", "compose", "down"])
      print("✅ Services stopped")
    except Exception as e:
      print(f"\n❌ Error: {e}")
      print("🛑 Stopping services...")
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