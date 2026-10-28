# AWS College Cloud Lab - Frontend and Backend

A simple lab registration app for your college submission. You create the Ubuntu EC2 instance yourself.

## What is included

- **Frontend:** registration form, class list, search, delete, and connection status using HTML/CSS/JavaScript.
- **Backend:** Flask REST API with input validation and duplicate roll-number checking.
- **Storage:** SQLite saved in a Docker volume, so records survive a restart or redeployment.
- **Deployment:** Nginx frontend and Python backend in two Docker containers.

```text
Browser -> Nginx (port 80) -> Flask API -> SQLite database
```

## Run on your own computer

Start Docker Desktop, then double-click **RUN.cmd**. Open **http://localhost:8088/**.

Use **STOP.cmd** to stop it; saved registrations are kept. If you prefer PowerShell:

```powershell
cd 'C:/Users/SHAYANTAN BISWAS/Desktop/ITLAB/AWSDockerLab'
$env:WEB_PORT = '8088'
$env:BIND_ADDRESS = '127.0.0.1'
docker compose -p college-lab up -d --build --wait
```

## Run on your EC2 instance

### 1. Create EC2

Use **Ubuntu Server 24.04 LTS, x86_64**, a public IPv4 address, and an instance size suitable for your AWS account. Check its displayed cost.

Security group: allow **SSH / TCP 22 / My IP** and **HTTP / TCP 80 / Anywhere IPv4**. The instance needs outbound internet access. Keep your downloaded `.pem` key outside this project.

### 2. Open the AWS browser terminal

In the EC2 console, select your instance, click **Connect**, select **EC2 Instance Connect**, and connect as **ubuntu**.

For a fresh installation, run these commands in that AWS terminal:

```bash
sudo apt-get update
sudo apt-get install -y git
git clone https://github.com/Shayantan1012/AWSDockerLab.git
cd AWSDockerLab
bash setup.sh
```

Open **http://YOUR_EC2_PUBLIC_IP/**. Try adding a student, searching, refreshing, and deleting the registration. Only port 80 needs public access for the app; the backend stays on Docker's private network.

## Updating an existing deployment

After committing updated project files to your GitHub repository, run these commands in the AWS browser terminal:

```bash
cd ~/AWSDockerLab
git pull
bash deploy.sh
```

For the already-cloned project, use `cd ~/AWSDockerLab`; you do not need to clone it again. Deployment is manual. The script rebuilds both containers while preserving saved registrations.

## Files and API

| File | Purpose |
|---|---|
| index.html, styles.css, app.js | Frontend |
| backend/app.py | Flask API and SQLite operations |
| backend/test_app.py | Backend tests |
| nginx.conf | Frontend server and API proxy |
| compose.yaml | Runs both containers and stores data |
| setup.sh / deploy.sh | EC2 setup and redeployment |

API: `GET /api/health`, `GET /api/registrations`, `POST /api/registrations`, and `DELETE /api/registrations/ID`.

Example JSON for adding a student:

```json
{"name": "Ananya Sharma", "roll_number": "CSE101", "department": "CSE"}
```

## Check and submit

- Container status: `sudo docker compose -p college-lab ps`
- Logs: `sudo docker compose -p college-lab logs --tail 50`
- API check: `curl http://localhost/api/health`
- Manual redeploy on EC2: `bash deploy.sh`
- Stop without deleting data: `sudo docker compose -p college-lab stop`

If the public page is unreachable, check the instance public IP and HTTP security-group rule.

Fill in **LAB-REPORT.md**. Submit screenshots of the EC2 instance, security-group rules, running containers, and frontend with saved registrations. Include a screenshot of the API health response. Recreate your submission ZIP after adding your report and screenshots. Do not include keys or local runtime files.

This is a college demo without login; use sample student details. After your demonstration, terminate the lab instance and review remaining AWS disks/IP resources and billing.
