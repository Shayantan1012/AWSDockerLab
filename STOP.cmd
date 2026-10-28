@echo off
cd /d "%~dp0"
set WEB_PORT=8088
set BIND_ADDRESS=127.0.0.1
docker compose -p college-lab stop
echo Website stopped. Saved registrations are preserved.
pause
