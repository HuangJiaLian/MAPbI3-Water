#!/bin/bash

simulation_type=cluster
mkdir -p $simulation_type
# Copy trajectory 
cp ../06_aimd/Cluster/nvt-pos-1.xyz $simulation_type/nvt-pos-1-222.xyz

simulation_type=bulk
mkdir -p $simulation_type
# Copy trajectory 
cp ../06_aimd/Bulk/nvt-pos-1.xyz $simulation_type/nvt-pos-1-222.xyz
