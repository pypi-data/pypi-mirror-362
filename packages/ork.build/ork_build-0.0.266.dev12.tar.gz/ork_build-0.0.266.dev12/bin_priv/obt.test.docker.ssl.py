#!/usr/bin/env python3

from obt import command 

svr_cmd = "_obt.test.docker.ssl.server.py"
cli_cmd = "_obt.test.docker.ssl.client.py"
 
# launch both in side by side tmux panes
command.run(["tmux", "new-session", "-d", "-s", "ssltest", "-n", "server", "python3", svr_cmd])
command.run(["tmux", "split-window", "-h", "-t", "ssltest:server", "-p", "50", "python3", cli_cmd])
command.run(["tmux", "select-layout", "-t", "ssltest:server", "even-horizontal"])
command.run(["tmux", "attach-session", "-t", "ssltest"])