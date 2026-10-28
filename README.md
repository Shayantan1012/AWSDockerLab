# AWS College Cloud Lab - Frontend, Backend and CI/CD

A simple lab registration app for your college submission. You create the Ubuntu EC2 instance yourself.

## What is included

- **Frontend:** registration form, class list, search, delete, and connection status using HTML/CSS/JavaScript.
- **Backend:** Flask REST API with input validation and duplicate roll-number checking.
- **Storage:** SQLite saved in a Docker volume, so records survive a restart or redeployment.
- **Deployment:** Nginx frontend and Python backend in two Docker containers.
- **CI/CD:** GitHub Actions tests and deploys the app when you push to `main`.

```text
Browser -> Nginx (port 80) -> Flask API -> SQLite database
GitHub push -> Runner on EC2 -> Tests -> Deploy frontend + backend
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

### 2. Upload and connect

Replace your private-key path and EC2 public IP in Windows PowerShell:

```powershell
cd 'C:/Users/SHAYANTAN BISWAS/Desktop/ITLAB'
$key = 'C:/path/to/college-key.pem'
$ec2Ip = 'YOUR_EC2_PUBLIC_IP'
scp -i "$key" -r ./AWSDockerLab "ubuntu@${ec2Ip}:~/"
ssh -i "$key" "ubuntu@$ec2Ip"
```

Upload a clean extracted copy of the submission ZIP to avoid copying local `.venv` files or databases. Inside the SSH terminal:

```bash
cd ~/AWSDockerLab
bash setup.sh
```

Open **http://YOUR_EC2_PUBLIC_IP/**. Try adding a student, searching, refreshing, and deleting the registration. Only port 80 needs public access for the app; the backend stays on Docker's private network.

## Set up CI/CD once

1. Create an empty **private GitHub repository** called `aws-college-lab`.
2. Push the **contents** of this project as the repository root, including `.github/workflows/deploy.yml`:

```powershell
cd 'C:/Users/SHAYANTAN BISWAS/Desktop/ITLAB/AWSDockerLab'
git init
git add .
git commit -m "College frontend backend and CI/CD"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/aws-college-lab.git
git push -u origin main
```

3. In GitHub, open **Settings > Actions > Runners > New self-hosted runner**. Select **Linux, x64**.
4. In your EC2 SSH terminal, run `cd ~`, then run the Download and Configure commands shown by GitHub. Add the label **ec2-lab** when prompted. Use the `ubuntu` account; do not run `config.sh` with sudo.
5. In `~/actions-runner`, run:

```bash
sudo ./svc.sh install ubuntu
sudo ./svc.sh start
```

6. Open **Actions > AWS EC2 CI-CD > Run workflow** and select `main`. Later pushes to `main` run it automatically.

CI starts a separate test stack on local port 8081, runs six backend tests, and checks the frontend and API. It removes only its temporary test data. CD updates the actual app while preserving its registrations volume. No AWS access keys are required in GitHub.

To demonstrate a change, edit text in `index.html`, then commit and push. Keep the title `AWS EC2 Docker Lab` because the pipeline uses it for a page check. Refresh the public website after the workflow succeeds.

## Files and API

| File | Purpose |
|---|---|
| index.html, styles.css, app.js | Frontend |
| backend/app.py | Flask API and SQLite operations |
| backend/test_app.py | Backend tests |
| nginx.conf | Frontend server and API proxy |
| compose.yaml | Runs both containers and stores data |
| setup.sh / deploy.sh | EC2 setup and redeployment |
| .github/workflows/deploy.yml | CI/CD pipeline |

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

If a pipeline is queued, check the runner is online with label `ec2-lab`. If the public page is unreachable, check the instance public IP and HTTP security-group rule.

Fill in **LAB-REPORT.md**. Submit screenshots of the EC2 instance, security-group rules, running containers, successful pipeline, and frontend with saved registrations. Include a screenshot of the API health response. Recreate your submission ZIP after adding your report and screenshots. Do not include keys or local runtime files.

This is a college demo without login; use sample student details. After your demonstration, terminate the lab instance, remove the GitHub runner, and review remaining AWS disks/IP resources and billing.

Reference: [GitHub runner setup](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners).
