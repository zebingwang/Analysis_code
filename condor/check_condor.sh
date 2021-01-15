#!/usr/bin/env bash

message="Real time"

for dir in $(ls ./condor_out/*.log)
do
  if ! (tail $dir -n 2 | grep "$message">/dev/null)
  then
    echo $dir" failed"
  fi

done
