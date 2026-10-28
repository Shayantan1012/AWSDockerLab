#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Remove only the old single-container version when upgrading this lab.
if sudo docker container inspect college-web > /dev/null 2>&1; then
    sudo docker rm -f college-web
fi
sudo docker compose -p college-lab up -d --build --wait
port="${WEB_PORT:-80}"
curl --fail --silent --show-error "http://127.0.0.1:${port}/api/health" | grep -q 'connected'
sudo docker compose -p college-lab ps
echo "Deployment verified locally. Open http://YOUR_EC2_PUBLIC_IP/ in your browser."
