# Internet Technology Lab 6 - Cloud Services
## Manual Frontend and Backend Deployment on AWS EC2

**Name:** ____________________  
**Roll number:** ____________________  
**Date:** ____________________

### Aim

To manually deploy a containerized college lab registration application on an Ubuntu EC2 instance and access it through the public IP address.

### Tools

AWS EC2, Ubuntu, Docker Compose, Nginx, HTML/CSS/JavaScript, Python Flask and SQLite.

### Architecture

Browser -> Nginx frontend (HTTP 80) -> Flask backend API -> SQLite database in a Docker volume.


### Procedure

1. Create an Ubuntu EC2 instance and allow SSH from My IP and HTTP from Anywhere IPv4.
2. Connect through the AWS EC2 browser terminal, clone the GitHub project and run `bash setup.sh` inside its directory.
3. Open the EC2 public IP and add a registration using the frontend form.
4. Verify that search, delete and refresh work and `/api/health` reports a database connection.
5. To deploy later changes, update the GitHub files, then run `git pull` and `bash deploy.sh` on the instance.
6. Restart the app and verify that saved records persist.

### Observations

| Item | Actual result |
|---|---|
| EC2 instance ID / public IP | |
| Frontend URL | |
| Backend health response | |
| Add, search and delete results | |
| Records after restart | |
| GitHub repository URL | |

Attach screenshots of the EC2 instance, security group, running containers, frontend with sample registrations and API health response.

### Result

Record the observed frontend, backend and manual deployment outcome after execution: ____________________.

Fill in this report using the actual results from your EC2 instance.
