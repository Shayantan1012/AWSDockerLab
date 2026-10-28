#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Run this on your fresh Ubuntu EC2 instance.
sudo apt-get update
sudo apt-get install -y docker.io docker-buildx docker-compose-v2 curl git
sudo systemctl enable --now docker

bash deploy.sh
