#!/bin/bash

mongoBin=$(which mongo);

test -e "$mongoBin" || { echo "No \"mongo\" binary found"; exit 1; }

mongo mlb_stats_dev <<<"
db.tex.find({

},{
  'team': 1,
}).sort({'stats_loader_timestamp':-1}).limit(1).pretty();
"

