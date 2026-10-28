# Internet Technology Lab 6 - Cloud Services
## Frontend and Backend Deployment on AWS EC2 with CI/CD

**Name:** ____________________  
**Roll number:** ____________________  
**Date:** ____________________

### Aim

To deploy a containerized college lab registration application on an Ubuntu EC2 instance and automate testing and deployment using GitHub Actions.

### Tools

AWS EC2, Ubuntu, Docker Compose, Nginx, HTML/CSS/JavaScript, Python Flask, SQLite and GitHub Actions.

### Architecture

Browser -> Nginx frontend (HTTP 80) -> Flask backend API -> SQLite database in a Docker volume.

GitHub push -> Self-hosted runner on EC2 -> Build and tests -> Deploy frontend and backend.

### Procedure

1. Create an Ubuntu EC2 instance and allow SSH from My IP and HTTP from Anywhere IPv4.
2. Upload the project, connect using SSH and run `bash setup.sh`.
3. Open the EC2 public IP and add a registration using the frontend form.
4. Verify that search, delete and refresh work and `/api/health` reports a database connection.
5. Push the project to a private GitHub repository and register the EC2 runner with label `ec2-lab`.
6. Run the workflow. Edit the page, push to `main`, and check that the website updates after successful tests.
7. Restart the app and verify that saved records persist.

### Observations

| Item | Actual result |
|---|---|
| EC2 instance ID / public IP | |
| Frontend URL | |
| Backend health response | |
| Add, search and delete results | |
| Records after restart | |
| GitHub repository URL | |
| Successful workflow URL | |

Attach screenshots of the EC2 instance, security group, running containers, frontend with sample registrations, API health response and green CI/CD pipeline.

### Result

Record the observed frontend, backend and pipeline outcome after execution: ____________________.

EC2 deployment and GitHub execution require your instance and repository. Fill in this report using your actual results.
