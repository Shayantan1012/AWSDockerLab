@echo off
cd /d "%~dp0"
set WEB_PORT=8088
set BIND_ADDRESS=127.0.0.1
docker compose -p college-lab up -d --build --wait
if errorlevel 1 (
  echo Start Docker Desktop, then try again.
  pause
  exit /b 1
)
echo Open http://localhost:8088/
pause
