#!/usr/bin/env bash

set -euo pipefail

# Tell apt-get we're never going to be able to give manual
# feedback:
export DEBIAN_FRONTEND=noninteractive

apt clean

# Update the package listing, so we know what packages exist:
apt update

# Install security updates:
apt -y upgrade

# Install a new package, without unnecessary recommended packages:
apt -y install --no-install-recommends build-essential graphviz graphviz-dev tini

# Delete cached files we don't need anymore:
apt clean
rm -rf /var/lib/apt/lists/*
