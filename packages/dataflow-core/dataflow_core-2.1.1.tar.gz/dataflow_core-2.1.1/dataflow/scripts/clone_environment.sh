#!/bin/bash
set -e

source_env_name=$1
target_env_path=$2

# Use an isolated conda package cache to avoid concurrency issues
export CONDA_PKGS_DIRS=$(mktemp -d)
# to delete conda package cache after script finishes
trap 'rm -rf "$CONDA_PKGS_DIRS"' EXIT

# 1. Cloning conda env
conda create --clone ${source_env_name} --prefix ${target_env_path} --yes

echo "Environment Creation Successful"