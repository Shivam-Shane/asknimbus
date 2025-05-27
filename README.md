# Asknimbus

Asknimbus is a chatbot that provides answers based on AWS documentation and AWS re:Post Knowledge Center data. It leverages Retrieval-Augmented Generation (RAG) with Pinecone vector storage for efficient content retrieval, Upstash Redis for caching user messages and responses, and a Django backend hosted as a Docker container on an AWS EC2 instance. The frontend, built with React, is deployed separately and communicates with the backend via cross-origin API calls.

## Features


Knowledge Base: Answers queries using AWS documentation and AWS re:Post Knowledge Center data.

1. RAG Pipeline: Uses Pinecone vector storage for semantic search and retrieval.

2. Caching: Upstash Redis caches user messages and responses for improved performance.

3. Backend: Django-based API running in a Docker container on EC2.

4. Frontend: React-based UI, deployed separately, interacting with the backend via API.

5. Logging: Integrated with Grafana Loki for centralized log management.

## Architecture

Frontend: React application hosted on Vercel (asknimbus.vercel.app), making API calls to the backend.


Backend: Django application in a Docker container on EC2, accessible via https://portfoliobackend.servebeer.com/asknimbus/api/, is Ec2 instance IP mapped using NO IP free domain name provider for better accessible of api to frontend

Vector Storage: Pinecone API for RAG-based content retrieval.

Cache: Upstash Redis for storing user messages and responses.

Deployment: EC2 instance with Docker Compose, Nginx for routing, and Let’s Encrypt SSL.

API Endpoints


GET /asknimbus/api/healthcheck/: Checks backend health.



POST /asknimbus/api/chat/: Handles chatbot queries and responses.

## Contributing

Forks and contributions are welcome! Please submit pull requests or open issues for bugs, features, or improvements.

## Installation

For setup and installation instructions, see INSTALLATION.md.

## License

MIT License

## Contact

For questions, suggestions, or support, reach out at 
- **sk0551460@gmail.com** 
- **shivam.hireme@gmail.com**.

## Support the Project

Help support continued development and improvements:

- **Follow on LinkedIn**: Stay connected for updates – [LinkedIn Profile](https://www.linkedin.com/in/shivam-hireme/)
- **Buy Me a Coffee**: Appreciate the project? [Buy Me a Coffee](https://buymeacoffee.com/shivamshane)
- **Visit my Portfolio**: [Shivam's Portfolio](https://shivam-portfoliio.vercel.app/)