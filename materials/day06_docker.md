# Docker

As an example, we'll use this repo: https://github.com/open-cu/youarebot-classifier

In modern software development, one of the main challenges is to guarantee application portability, scalability, and isolation. **[Docker](https://docs.docker.com/)** is a containerization platform that lets you package, distribute, and run applications in standardized environments called *containers*.

**Containerization** is a technology that runs applications in isolated environments that include every necessary dependency—libraries, system utilities, code, and configuration. Unlike traditional virtualization, where each application runs inside its own virtual machine (VM) with a fully fledged operating system, containers share the host-OS kernel, making them far lighter and faster.

<p align="center">
  <img src="./assets/container_evolution.png" alt="Virtualization vs Containers" width="1000">
</p>

### Virtualization

* **Pros**
  * Stronger isolation between applications  
  * Ability to run different operating systems on the same server  
* **Cons**
  * High resource overhead (each VM includes an entire OS)  
  * Slower startup compared with containers  

### Containerization

* **Pros**
  * Lightweight (no duplicate OS needed)  
  * Rapid deployment and scaling  
  * Lower resource usage  
* **Cons**
  * Weaker isolation than VMs (because the kernel is shared)  
  * Must match the host OS (e.g., Windows containers can’t run on Linux without extra tooling)  

<br>

<p align="center">
  <img src="./assets/dockerstructure.jpeg" alt="Docker Structure" width="1000">
</p>

### Key reasons Docker took off

* **Standardized API**  
  * Docker provides a single interface for working with containers, simplifying automation and CI/CD integration.  
  * Commands such as `docker build`, `docker pull`, and `docker run` make container management straightforward.  

* **Full-featured ecosystem**  
  * The Docker Registry (Docker Hub or private registries) stores and distributes images.  
  * The Docker Daemon handles low-level container management in the background.  

* **Simplified development & deployment**  
  * Developers work in identical environments regardless of host OS.  
  * Layered file systems let images be stored and downloaded efficiently.  

* **Effortless scaling**  
  * Docker integrates easily with Kubernetes and other orchestrators, making it indispensable in cloud setups.  

* **Multi-platform support**  
  * Runs on Windows, macOS, and Linux.  

### Core Docker concepts

* **Dockerfile** – the *recipe* for building an image.  
  * Describes the dependencies and configuration a container needs.  
  * Example:  
    ```dockerfile
    FROM python:3.9  
    COPY app.py /app/app.py  
    CMD ["python", "/app/app.py"]
    ```  
  * Used to create an image via `docker build`.

* **Image** – a *snapshot* of a file system built from a Dockerfile.  
  * Contains all dependencies (libraries, executables, configs).  
  * Stored in a **Docker Registry** (e.g., **Docker Hub**).  
  * Started as a container with `docker run`.

* **Container** – a *running instance* of an image.  
  * Runs in isolation while sharing host resources.  
  * Can be started, stopped, removed (`docker start`, `docker stop`, `docker rm`).  

* **Docker Daemon** – the background process that manages images and containers.  
  * Executes `docker build`, `docker run`, `docker pull`, and other commands.  

* **Docker Registry** – a repository for images.  
  * Allows images to be pulled (`docker pull`) and pushed (`docker push`).  

### Relationship between the entities
1. **Write a Dockerfile** →  
2. **Build an image** (`docker build`) →  
3. **(Optional) Push the image to a registry** (`docker push`) →  
4. **Run a container** (`docker run`).  

<p align="center">
  <img src="./assets/docker_process.webp" alt="Docker image process" width="1000">
</p>

## Docker Cheat Sheet – frequently used commands

```bash
# List all containers (including stopped ones)
docker ps -a

# Build an image from a Dockerfile
docker build -t <image_name> .

# Run a container in detached mode
docker run -d <image_name>

# Run a container with an interactive terminal
docker run -it <image_name> /bin/bash

# List all images
docker images

# Stop a container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# Remove an image
docker rmi <image_id>

# Inspect detailed container information
docker inspect <container_id>

# Execute a command inside a running container
docker exec -it <container_id> <command>

# View container logs
docker logs <container_id>

# Stop all containers
docker stop $(docker ps -q)

# Remove all stopped containers
docker container prune

# Remove dangling images (not used by any container)
docker image prune

# Publish a container port on the host.
# Requests to host_port are forwarded to container_port inside the container.
docker run -p <host_port>:<container_port> <image_name>

# Display real-time resource usage statistics
docker stats

# Rename a container
docker rename <old_name> <new_name>

# Create and run a container with a volume.
# Files in host_directory are accessible inside the container at container_directory
docker run -v <host_directory>:<container_directory> <image_name>

# Display Docker system information
docker info

# Run a container with resource limits (e.g., CPU and memory)
docker run --memory="500m" --cpus="1.0" <image_name>

# Run a container in the host network namespace (no port mapping needed)
docker run --net=host <image_name>
```

## Packaging a service with Docker

Below is an example of containerizing our **turing\_test\_service**.

**Dockerfile**

```dockerfile
# Use an official Python runtime as the base image
FROM python:3.12.8-bookworm

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.0.1
ENV POETRY_VIRTUALENVS_CREATE=false

# Install Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Working directory inside the container
WORKDIR /app

# Copy pyproject.toml and poetry.lock (if present)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies with Poetry
RUN poetry install --no-root --no-cache --only main

# Copy service source code and configs
COPY turing_test_service /app/turing_test_service
COPY config /app/config

# Expose the port used by uvicorn
EXPOSE 8000

# Command to start the FastAPI service with uvicorn
CMD ["poetry", "run", "uvicorn", "turing_test_service.api.main:app", \
    "--host", "0.0.0.0", "--port", "8000", "--log-config", "./config/logging_config.yaml"]
```

We start from the official Python image, install the required Poetry version, and use it to install project dependencies directly into the system environment (no virtualenv). Then we copy the source code and config files into the container and launch the service.

* Build the image: `docker build -t turing_test_service .`
* Run the container and publish port 8000: `docker run -d -p 8000:8000 turing_test_service`

Afterwards you can query the service, e.g. with **curl**:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"chat_id": 42, "messages": [
        {"message_id": 0, "text": "How about the money?", "participant_id": 0},
        {"message_id": 1, "text": "Who are you calling?", "participant_id": 1}
      ]}'
```

# Docker Compose

**[Docker Compose](https://docs.docker.com/compose/)** is a tool that simplifies management of multi-container Docker applications. It lets you describe and start several interrelated containers through a single configuration file, making deployment more convenient and controlled. Instead of running each container separately with `docker run`, Docker Compose allows you to define containers, their interactions, dependencies, networks, and volumes in one YAML file.

```bash
# Start all services in detached mode
docker compose up -d

# Start all services (stream logs to the console)
docker compose up

# Stop and remove all running services, networks, and volumes
docker compose down

# Stop services without removing containers
docker compose stop

# Restart previously stopped services
docker compose start

# Recreate and restart all services
docker compose restart

# List running services
docker compose ps

# Show logs from all services
docker compose logs

# Follow logs in real time
docker compose logs -f

# Build images for all services
docker compose build

# Build images and start services
docker compose up --build

# Pull the latest versions of images referenced in the compose file
docker compose pull

# Execute a command inside a running container
docker compose exec <service> <command>
# Example: open a shell inside the "app" container
docker compose exec app bash
```

A `docker-compose.yaml` file in this repository defines everything needed to run the service:

```yaml
version: "3.9"

services:
  turing-test-service:
    build: .
    container_name: turing-test-service
    env_file:
      - .env
    ports:
      - "443:8000"
    networks:
      - student_net
    deploy:
      resources:
        limits:
          memory: 4G

networks:
  student_net:
    driver: bridge
```

After launching with `docker compose up`, the service becomes available on port 443 (because the configuration maps `"443:8000"`).

 
 