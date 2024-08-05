## Getting Started
### Requirements
For building and running the application you need:

- [Python 3.10](https://www.python.org/downloads/release/python-3100/)

### Installation
```bash
$ git clone https://github.com/Rimember/ringchat.git
$ cd ringchat
```

### Frontend
```bash
$ cd frontend
$ npm install
$ npm run dev

> frontend@0.1.0 dev
> next dev

  ▲ Next.js 14.2.5
  - Local:        http://localhost:3000

 ✓ Starting...
 ✓ Ready in 3.6s
 ○ Compiling / ...
 ✓ Compiled / in 14.1s (489 modules)
 GET / 200 in 14606ms
```

### Backend
```bash
$ cd backend
$ poetry install

# Manually create OPENAI_API_KEY configuration file
$ vi .env

# Run backend
$ uvicorn backend.main:app

# Send and receive HTTP queries to the backend using the curl command
$ curl -X POST -H "Content-Type: application/json" -d '{"question": "What is a lambda function in Python?"}' http://127.0.0.1:8000/ask
```

## Deploy(Docker container)
### Frontend
```bash
$ cd frontend
$ sudo docker build -t frontend .
$ sudo docker run -p 3000:3000 --name=frontend frontend
```

### Backend
```bash
$ cd backend
$ sudo docker build -t backend .
$ sudo docker run -p 8000:8000 --name=backend backend
```

### RingChat(frontend + backend)
```bash
# When installed with Docker compose plugin
$ sudo docker compose up
```

## Note : Remove Docker container
### Check running container
```bash
$ sudo docker ps
```

### Check for stopped containers
```bash
$ sudo docker ps -a
```

### Delete container
```bash
$ sudo docker rm {container id}
```

### Delete all containers
```bash
$ sudo docker rm `sudo docker ps -a -q`
```

## Note : Remove Docker image
### Check current image
```bash
$ sudo docker images
```

### Delete image
```bash
$ sudo docker rmi {image id}
```

### If you add the -f option, the container will also be forcefully deleted.
```bash
$ sudo docker rmi -f {image id}
```