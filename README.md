AI Blog Generator
Generate full blog posts from YouTube videos using AssemblyAI for transcription and GROQ AI for content generation — all served via a load-balanced, multi-container Dockerized Django app.

✨ Features
🔗 Accepts YouTube video links as input

🎧 Extracts and transcribes audio using AssemblyAI

📝 Generates long-form blog content using GROQ's LLaMA 3 model

💾 Authenticated users can view and save generated posts

🐳 Dockerized for easy deployment

⚖️ Load-balanced using HAProxy (Round Robin across web-01 and web-02)

🎨 Styled with TailwindCSS

🗂️ Project Structure
bash
Copy
Edit
AI-Blog/
├── backend/
│   └── ai_blog_app/
│       ├── templates/
│       ├── static/
│       ├── views.py
│       ├── models.py
│       ├── urls.py
│       └── ...
│   └── manage.py
├── Dockerfile
├── docker-compose.yml
├── .env
└── load_balancer/
    └── haproxy.cfg
🚀 How It Works
User pastes a YouTube video link.

The app downloads and transcribes audio using AssemblyAI.

The transcript is sent to the GROQ API, which generates a blog article.

The article is displayed in the frontend and stored in the database.

Users can log in and view previously generated posts.

🛠️ Setup & Installation

🔧 Requirements
Docker & Docker Compose

AssemblyAI and GROQ API keys

🔐 Create .env file
env
Copy
Edit
ASSEMBLYAI_API_KEY=your_assemblyai_key
GROQ_API_KEY=your_groq_key
🐳 Build & Run the App
bash
Copy
Edit
docker-compose up --build
The app will be available at: http://localhost

Load balancing via HAProxy (requests routed to web-01 and web-02 containers)

🧪 API Endpoints
Method	Endpoint	Description
POST	/generate-blog/	Generate blog post from YouTube link
GET	/blog-list	View saved blog posts (authenticated)
GET	/blog-details/<id>	View specific blog post

👤 Authentication
Sign up or log in to access the homepage

Session-based auth (Django default)

Blog posts are user-specific

Dockerized Deployment with HAProxy Load Balancer
This project is a Django-based AI blog generation app that uses an external API to generate blog content. The application is containerized using Docker and deployed using a load-balanced setup with HAProxy to distribute traffic between two instances (web-01, web-02). PostgreSQL is used as the backend database.

📦 Docker Images
Image Name	Description
plouis17/ai_blog_web:v1	Django web app for blog generation
haproxy:2.4	Load balancer container
postgres:15	Database container

📁 Directory Structure
bash
Copy
Edit
ai_blog_app/
├── ai_blog_app/              # Django core
├── blog_generator/           # Blog generation logic
├── templates/                # HTML templates
├── media/                    # Uploaded/generated media
├── load_balancer/
│   ├── haproxy.cfg           # HAProxy config
│   └── Dockerfile            # Dockerfile for HAProxy
├── docker-compose.yml        # Optional: local orchestration
├── Dockerfile                # Dockerfile for web app
├── manage.py
└── requirements.txt
⚙️ How to Build and Push Docker Images
1. Build and Push Web App Image
bash
Copy
Edit
# From the root project directory
docker build -t plouis17/ai_blog_web:v1 .
docker plouis17/ai_blog_web:v1
2. Build and Push Load Balancer Image
bash
Copy
Edit
cd load_balancer/
docker build -t plouis17/ai_blog_web:v1 .
docker push plouis17/ai_blog_web:v1
🚀 Deployment Instructions
Assuming you're using 3 containers: web-01, web-02, and lb-01.

1. On Web-01 and Web-02
bash
Copy
Edit
# Pull the web image
docker pull plouis17/ai_blog_web:v1

# Run the container (different port and SERVER_NAME for each)
docker run -d --name web-01 --restart unless-stopped \
  -e SERVER_NAME=web-01 \
  -p 8081:8080 plouis17/ai_blog_web:v1

# On web-02 (change SERVER_NAME and port)
docker run -d --name web-02 --restart unless-stopped \
  -e SERVER_NAME=web-02 \
  -p 8082:8080 plouis17/ai_blog_web:v1
Test manually:

bash
Copy
Edit
curl http://localhost:8081/
# → This response is from web-01

curl http://localhost:8082/
# → This response is from web-02
2. On Load Balancer (Lb-01)
a. Sample haproxy.cfg
haproxy
Copy
Edit
global
    daemon
    maxconn 256

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http_front
    bind *:80
    default_backend webapps

backend webapps
    balance roundrobin
    server web01 web-01:8080 check
    server web02 web-02:8080 check
b. Dockerfile for HAProxy (in load_balancer/)
Dockerfile
Copy
Edit
FROM haproxy:2.8
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg
c. Run Load Balancer Container
bash
Copy
Edit
docker run -d --name lb-01 --restart unless-stopped \
  --network host \
  plouis17/ai_blog_haproxy:latest
You can also use Docker networks and specific IPs instead of --network host, depending on your setup.

✅ Testing Load Balancing
Run the following command several times:

bash
Copy
Edit
curl http://localhost/
Expected output:

csharp
Copy
Edit
This response is from web-01
This response is from web-02
This response is from web-01
...
This confirms that HAProxy is distributing traffic between the two containers using the round-robin method.

🔐 Handling Secrets (Optional Hardening Step)
To avoid exposing API keys or database credentials in the image:

Use .env files or -e flags with Docker

Keep secrets out of source control using .gitignore

Use os.environ.get() in Django settings.py

Docker Containers
https://hub.docker.com/repository/docker/plouis17/ai_blog_web/general
https://hub.docker.com/repository/docker/plouis17/ai_blog_haproxy/general

📹 Demo Video
https://youtu.be/UJknByj9tfU

📄 API Used
External API used for generating blog content.

https://www.assemblyai.com/docs/api-reference/overview
https://console.groq.com/docs/api-reference

🙌 Acknowledgements
Django

PostgreSQL

Assembly AI

Groq Cloud

Docker

HAProxy




 Author
Louis Nsigo



