#!/usr/bin/env python3 

import os, proctools, argparse, sys
from obt import path, deco
deco = deco.Deco()

os.environ["DOCKER_BUILDKIT"] = "1"

# Parse arguments (including those passed from OBT)
parser = argparse.ArgumentParser(description='ZMQ SSL Example Docker Builder (OBT compatible)')
parser.add_argument('--service', choices=['zmq-server', 'ssl-proxy', 'all'], 
                   default='all', help='Which service to build')

# Parse known args to handle OBT's build_args gracefully
args, unknown_args = parser.parse_known_args()

print(f"Building ZMQ SSL Example - Service: {args.service}")
if unknown_args:
    print(f"Additional build args: {unknown_args}")

# Use docker compose build for COMPOSITE type consistency
cmdlist = ["docker", "compose", "build"]

# Add service-specific build if requested
if args.service != 'all':
    cmdlist.append(args.service)

# Add any additional build args from OBT
cmdlist.extend(unknown_args)

print(f"Running: {' '.join(cmdlist)}")
proctools.sync_subprocess(cmdlist)

print("Build complete!")
print("Services built:")
if args.service in ['zmq-server', 'all']:
    print("  - zmq-server (ZMQ REP server)")
if args.service in ['ssl-proxy', 'all']:
    print("  - ssl-proxy (stunnel SSL termination)")
print("Use 'docker compose up' to start the services")
