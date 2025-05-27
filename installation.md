# Asknimbus Installation Guide

This guide covers installing and running Asknimbus on a Windows server as a standard Django and npm application, or deploying it on Linux using Docker. Both setups require a custom SSL certificate and updating the .env file for cross-origin requests.

## Prerequisites

- Windows Server:

Python 3.11+

Node.js 16+ and npm

Git

Custom SSL certificate (e.g., .pem files for fullchain and private key)


- Linux (Docker):

Docker and Docker Compose

Git

Custom SSL certificate

Python 3.11+ (for dependency installation)

- General:

Pinecone API key

Upstash Redis REST URL and token

Grafana Loki URL, user, and API key

## Windows Server Setup

Clone the Repository:

git clone <repository-url>
cd asknimbus

## Backend (Django):

Install dependencies:

cd backend
pip install -r requirements.txt

Update .env with your credentials and URLs:

SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-backend-domain,localhost
PINECONE_API_KEY=your-pinecone-key
PINECONE_INDEX_NAME=awsdata
UPSTASH_REDIS_REST_URL=your-redis-url
UPSTASH_REDIS_REST_TOKEN=your-redis-token
LOKI_URL=your-loki-url
LOKI_USER=your-loki-user
LOKI_API_KEY=your-loki-api-key
CORS_ALLOWED_ORIGINS=https://your-frontend-domain


Run the server:

python manage.py runserver 0.0.0.0:8000

## Frontend (React):

Install dependencies:

cd ../frontend
npm install

Update .env with the backend URL:

REACT_APP_BACKEND_URL=https://your-backend-domain/asknimbus/api/

Build and serve:

npm run build
npm start

SSL Configuration:

Use a reverse proxy (e.g., Nginx or IIS) to serve the app over HTTPS.

Configure your SSL certificate:

Place fullchain.pem and privkey.pem in a secure directory.


Update the reverse proxy to use these files (e.g., Nginx config):

ssl_certificate /path/to/fullchain.pem;
ssl_certificate_key /path/to/privkey.pem;

Ensure the backend and frontend URLs in .env match the HTTPS domain.

- CORS:

Verify CORS_ALLOWED_ORIGINS in the backend .env includes the frontend URL (e.g., https://your-frontend-domain).

- Test:

Access the frontend at https://your-frontend-domain.

Test the API:

curl https://your-backend-domain/asknimbus/api/healthcheck/

## Linux Docker Deployment

- Frontend (React):

Same as Windows: install dependencies, update .env, build, and deploy to a hosting service (e.g., Vercel).


Ensure REACT_APP_BACKEND_URL=https://your-backend-domain/asknimbus/api/.

SSL Configuration:

Place your SSL certificate files (fullchain.pem, privkey.pem) in /etc/letsencrypt/live/your-backend-domain/.

Update nginx/default.conf to reference these files:

ssl_certificate /etc/live/your-backend-domain/fullchain.pem;
ssl_certificate_key /etc/live/your-backend-domain/privkey.pem;

- Backend:

Clone or download the docker related files.(Dockerfile, docker-compose.yml)

Pull the latest image from: docker pull shivamshane/asknimbusbackend:latest

Start the containers using the docker-compose having docker-compose.yml file at path, make sure .env is also present on same location 

docker-compose up -d

CORS:

Ensure CORS_ALLOWED_ORIGINS includes the frontend URL.

- Test:

Access the frontend at https://your-frontend-domain.

Test the API:

curl https://your-backend-domain/asknimbus/api/healthcheck/

## Notes

Replace your-backend-domain and your-frontend-domain with your actual domains.

Ensure firewall rules allow ports 80 and 443.

For production, use a WSGI server (e.g., Gunicorn) for Django and a production-grade server for React.

Troubleshooting

Check container logs:

docker logs asknimbus_backend
docker logs nginx_proxy

Check Grafana logs for monitoring of application.

Verify CORS settings if cross-origin requests fail.


## Contact

For questions, suggestions, or support, reach out at 
- **sk0551460@gmail.com** 
- **shivam.hireme@gmail.com**.

## Support the Project

Help support continued development and improvements:

- **Follow on LinkedIn**: Stay connected for updates – [LinkedIn Profile](https://www.linkedin.com/in/shivam-hireme/)
- **Buy Me a Coffee**: Appreciate the project? [Buy Me a Coffee](https://buymeacoffee.com/shivamshane)
- **Visit my Portfolio**: [Shivam's Portfolio](https://shivam-portfoliio.vercel.app/)