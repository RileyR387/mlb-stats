# mlb-stats
Python dependency/distributable/deliverable demo project. Cache MLB stats from ESPN rest endpoints to Mongo - no useful output yet.

```shell

# review config
cat etc/get-stats-terminal.py.yaml

# create venv
make

# install to venv
make install

# show help
./venv/bin/get-stats-terminal.py

# demo it
./venv/bin/get-stats-terminal.py -c etc/get-stats-terminal.py.yaml -t tex

```
