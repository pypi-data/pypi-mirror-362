#!/bin/bash
set -e

IFS=',' read -r -a  libraries <<< $1
conda_env_path=$2
py_version=$3

# Use an isolated conda package cache to avoid concurrency issues
export CONDA_PKGS_DIRS=$(mktemp -d)
# to delete conda package cache after script finishes
trap 'rm -rf "$CONDA_PKGS_DIRS"' EXIT

# 1. Creating conda environment
conda create --prefix ${conda_env_path} --yes python=${py_version} 

# 2. Install user libraries
${conda_env_path}/bin/pip install --root-user-action ignore ${libraries[@]}      
