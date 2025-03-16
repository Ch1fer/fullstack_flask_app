# QR Code Generator  
This web application enables users to generate QR codes from input text and store them in a database. QR code records can be created, viewed, edited, and deleted.

## Features  
The web application runs in 3 separate Docker containers:
- **nginx_server** – Frontend container, serving as a reverse proxy that handles incoming requests and serves static files.
- **db** – Database container that stores QR code records and related data.
- **flask_app** – Backend application built with Flask, responsible for generating QR codes and processing API requests.

## Running the Project with Docker
1. Before starting the project, make sure you have the following files in your project directory:
   - `compose_prod.yml`
   - `start-app.sh`
   - `end-app.sh`

2. To start the project, run the following command in the Bash terminal:
   ```bash
   ./start-app.sh
   
3. After starting the project, you can access the application at:
http://localhost:8080/

4. To stop the project, run the following command in the Bash terminal:
    ```bash
   ./end-app.sh

repository: **https://github.com/Ch1fer/fullstack_flask_app**