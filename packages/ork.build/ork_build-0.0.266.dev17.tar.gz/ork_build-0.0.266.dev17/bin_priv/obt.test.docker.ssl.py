#!/usr/bin/env python3
 
from obt import command, tmux

##########################################################

session = tmux.Session("OBT_SSL_TEST")
session.command(["_obt.test.docker.ssl.server.py"])
session.command(["_obt.test.docker.ssl.client.py"])
session.execute()

