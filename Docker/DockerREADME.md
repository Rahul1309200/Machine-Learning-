# Docker Learning Notes

---

## Part 1: What is Docker?

### The Problem (Why Docker Exists)

Imagine you build a Python app on your laptop. It works perfectly. You send it to your friend — it crashes. Why?

Because your friend has:
- A different OS (Windows vs Mac vs Linux)
- Different Python version
- Missing libraries/packages

**Docker solves this.** It packages your app + everything it needs (OS, libraries, dependencies) into a single box called a **container**. Now it runs the same everywhere.

### Real-Life Analogy

Think of Docker like a **shipping container** (the metal boxes on cargo ships):
- Doesn't matter what's inside (clothes, electronics, food)
- Doesn't matter which ship carries it
- The container is standard — it fits everywhere

Docker does the same for software.

---

### Key Terms (Just 4 for now)

| Term | What it means | Analogy |
|------|--------------|---------|
| **Image** | A blueprint/recipe for your app | Like a cake recipe |
| **Container** | A running instance of an image | Like the actual cake made from the recipe |
| **Dockerfile** | Instructions to build an image | Like writing down the recipe steps |
| **Docker Hub** | Online store of pre-built images | Like an app store for Docker images |

---

## Part 2: Installing Docker

### On Mac:
1. Go to https://www.docker.com/products/docker-desktop/
2. Download "Docker Desktop for Mac"
3. Install it (drag to Applications)
4. Open Docker Desktop — wait for it to say "Running"

### Verify Installation:
```bash
docker --version
```
Output should look like:
```
Docker version 24.0.7, build afdd53b
```

---

## Part 3: Your First Docker Command

### Check if Docker is running:
```bash
docker info
```
This shows details about your Docker installation.

### Run your first container:
```bash
docker run hello-world
```

**What happens:**
1. Docker looks for the `hello-world` image on your computer
2. Doesn't find it → downloads it from Docker Hub
3. Creates a container from that image
4. Runs the container → prints a "Hello from Docker!" message
5. Container stops

**Output you'll see:**
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

---

## Part 4: Basic Docker Commands

### See all images on your computer:
```bash
docker images
```
Output:
```
REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
hello-world   latest    d2c94e258dcb   3 months ago   13.3kB
```

### See running containers:
```bash
docker ps
```
(Shows nothing if no container is currently running)

### See ALL containers (including stopped ones):
```bash
docker ps -a
```
Output:
```
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      NAMES
a1b2c3d4e5f6   hello-world   "/hello"   2 minutes ago    Exited (0) 2 minutes ago    happy_tesla
```

### Remove a container:
```bash
docker rm <container_id>
# Example:
docker rm a1b2c3d4e5f6
```

### Remove an image:
```bash
docker rmi <image_name>
# Example:
docker rmi hello-world
```

---

## Part 5: Running a Real Container (Ubuntu)

Let's run a full Ubuntu Linux inside a container:

```bash
docker run -it ubuntu bash
```

**Breaking down the command:**
- `docker run` → run a container
- `-it` → interactive mode (so you can type commands inside)
- `ubuntu` → the image to use
- `bash` → the command to run inside (open a terminal)

**Now you're INSIDE the container!** Your terminal changes to something like:
```
root@3f4a5b6c7d8e:/#
```

### Try some commands inside:
```bash
# Check the OS
cat /etc/os-release

# List files
ls

# Create a file
echo "Hello from inside Docker!" > myfile.txt

# Read the file
cat myfile.txt

# Exit the container
exit
```

**Important:** When you exit, the container stops. Any files you created inside are gone (unless you save them — we'll learn that later).

---

## Part 6: Pulling Images from Docker Hub

Docker Hub (hub.docker.com) has thousands of pre-built images.

### Pull an image without running it:
```bash
docker pull nginx
```
This downloads the Nginx web server image.

### Run Nginx:
```bash
docker run -d -p 8080:80 nginx
```

**Breaking down:**
- `-d` → run in background (detached mode)
- `-p 8080:80` → map port 8080 on YOUR computer to port 80 inside the container
- `nginx` → the image

**Now open your browser and go to:** http://localhost:8080

You'll see the Nginx welcome page! 🎉 You just ran a web server in 1 command.

### Stop the container:
```bash
# First find the container ID
docker ps

# Then stop it
docker stop <container_id>
```

---

## Summary So Far

| Command | What it does |
|---------|-------------|
| `docker --version` | Check Docker version |
| `docker run hello-world` | Run your first container |
| `docker images` | List all images |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker run -it ubuntu bash` | Run Ubuntu interactively |
| `docker pull nginx` | Download an image |
| `docker run -d -p 8080:80 nginx` | Run Nginx web server |
| `docker stop <id>` | Stop a container |
| `docker rm <id>` | Remove a container |
| `docker rmi <image>` | Remove an image |

---

---

## Part 7: Writing Your Own Dockerfile

Until now, we used images made by others (nginx, ubuntu). Now let's build our OWN image.

### What is a Dockerfile?

A Dockerfile is just a **text file** with step-by-step instructions telling Docker how to build your image. Like a recipe card.

### Let's Build: A Simple Python App in Docker

**Step 1: Create a project folder**
```bash
mkdir my-docker-app
cd my-docker-app
```

**Step 2: Create a simple Python file**

Create `app.py`:
```python
print("Hello! I'm running inside a Docker container! 🐳")
name = "Docker Learner"
print(f"Welcome, {name}!")
print("Python version:")

import sys
print(sys.version)
```

**Step 3: Create the Dockerfile**

Create a file called `Dockerfile` (no extension, capital D):
```dockerfile
# Step 1: Start from a base image (Python already installed)
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy your file from your computer INTO the container
COPY app.py .

# Step 4: Tell Docker what command to run when container starts
CMD ["python", "app.py"]
```

**Step 4: Build the image**
```bash
docker build -t my-python-app .
```

Breaking it down:
- `docker build` → build an image
- `-t my-python-app` → give it a name (tag)
- `.` → look for the Dockerfile in the current directory

**Step 5: Run YOUR image**
```bash
docker run my-python-app
```

Output:
```
Hello! I'm running inside a Docker container! 🐳
Welcome, Rahul!
Python version:
3.11.x (main, ...) [GCC ...]
```

🎉 You just built and ran your own Docker image!

---

### Understanding Each Dockerfile Instruction

| Instruction | What it does | Example |
|-------------|-------------|---------|
| `FROM` | Base image to start from | `FROM python:3.11-slim` |
| `WORKDIR` | Sets the folder inside container | `WORKDIR /app` |
| `COPY` | Copies files from your PC → container | `COPY app.py .` |
| `RUN` | Runs a command DURING build | `RUN pip install flask` |
| `CMD` | Command to run WHEN container starts | `CMD ["python", "app.py"]` |
| `EXPOSE` | Documents which port the app uses | `EXPOSE 5000` |

### Key Difference: RUN vs CMD

- `RUN` → executes during **build time** (installing packages, creating folders)
- `CMD` → executes when you **run the container** (starting your app)

```dockerfile
RUN pip install flask        # happens when building the image
CMD ["python", "app.py"]     # happens when you do 'docker run'
```

---

### Example 2: A Flask Web App in Docker (Hands-On)

Now let's build something real — a web app you can open in your browser!

**Step 1: Create a project folder**
```bash
mkdir <your-project-name>
cd <your-project-name>
```

**Step 2: Create `app.py`**
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Docker! 🐳</h1><p>This is my Flask app running in a container.</p>"

@app.route("/about")
def about():
    return "<h1>About</h1><p>I'm learning Docker from scratch!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

**Step 3: Create `requirements.txt`**
```
flask
```

**Step 4: Create `Dockerfile`**
```dockerfile
# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching — explained below)
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY app.py .

# Document the port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
```

**Your folder should look like:**
```
<your-project-name>/
├── Dockerfile
├── app.py
└── requirements.txt
```

**Step 5: Build the image**
```bash
docker build -t <your-image-name> .
```

**Step 6: Run it**
```bash
docker run -d -p 5000:5000 <your-image-name>
```

**Step 7: Open your browser**
- Go to http://localhost:5000 → You'll see "Hello from Docker! 🐳"
- Go to http://localhost:5000/about → You'll see the about page

**Step 8: When done, stop it**
```bash
docker ps                    # find the container ID
docker stop <container_id>   # stop it
```

🎉 You just built and ran a web app in Docker!

---

### Why We COPY requirements.txt Separately

Docker uses **layer caching**. Each instruction creates a layer:
```
Layer 1: FROM python:3.11-slim
Layer 2: WORKDIR /app
Layer 3: COPY requirements.txt .
Layer 4: RUN pip install -r requirements.txt  ← slow (downloads packages)
Layer 5: COPY app.py .
Layer 6: CMD [...]
```

If you only change `app.py`, Docker reuses layers 1-4 from cache and only rebuilds layer 5. This makes rebuilds **much faster** because it doesn't reinstall packages every time.

If you did `COPY . .` all at once, ANY file change would trigger a full `pip install` again. Slow! 🐌

---

### Useful Build Commands

```bash
# Build with a tag/version
docker build -t <image-name>:<version> .

# See build history of an image
docker history <image-name>

# List your images
docker images
```

---

### Complete Workflow Summary

```
1. Write your app code (app.py, etc.)
2. Write a Dockerfile (instructions to package it)
3. docker build -t <image-name> .              ← creates the image
4. docker run -d -p <port>:<port> <image-name> ← runs the container
5. Open browser → see your app!
```

---

---

## Part 8: Docker Volumes (Keeping Your Data Alive)

### The Problem

Remember when we ran Ubuntu and created a file inside?

```bash
docker run -it ubuntu bash
echo "important data" > myfile.txt
exit
```

That file is **gone**. When a container stops, everything inside it disappears. That's a problem if you're running a database or saving user uploads.

### The Solution: Volumes

A **volume** is a folder on YOUR computer that is connected to a folder INSIDE the container. Data saved there survives even after the container dies.

```
Your Computer                    Container
─────────────                    ─────────
/Users/you/mydata/ ◄──────────► /app/data/
  (permanent)        connected     (also permanent now!)
```

---

### Type 1: Named Volumes (Docker manages the storage)

**Create and use a volume:**
```bash
# Create a named volume
docker volume create mydata

# Run a container with the volume attached
docker run -it -v mydata:/app/data ubuntu bash
```

**Inside the container:**
```bash
cd /app/data
echo "This will survive!" > important.txt
exit
```

**Now run a NEW container with the same volume:**
```bash
docker run -it -v mydata:/app/data ubuntu bash
cat /app/data/important.txt
```

Output:
```
This will survive!
```

🎉 The data persisted across containers!

**Breaking down `-v mydata:/app/data`:**
```
-v mydata:/app/data
    │        │
    │        └── folder INSIDE the container
    │
    └── volume name (Docker manages where it's stored)
```

---

### Type 2: Bind Mounts (YOU choose the folder)

This connects a specific folder on your computer to the container:

```bash
docker run -it -v /Users/you/myproject:/app ubuntu bash
```

Now `/app` inside the container IS your `/Users/you/myproject` folder. Changes go both ways:
- Edit a file on your computer → it changes inside the container
- Create a file inside the container → it appears on your computer

**This is super useful for development!** You edit code on your machine, and the container sees the changes instantly.

**Hands-On: Use a Volume with Your Flask App (my-flask)**

We already built a Flask image earlier. Let's use a bind mount with it!

**Step 1: Go into your flask project folder**
```bash
cd my-flask-app
```

**Step 2: Run with a volume attached**
```bash
docker run -d -p 5000:5000 -v $(pwd):/app my-flask
```
- `$(pwd)` = your current directory (automatically fills in the full path)
- `-v $(pwd):/app` = connects your local folder ↔ container's `/app`

**Step 3: Open browser**
- Go to http://localhost:5000 → You see "Hello from Docker! 🐳"

**Step 4: Edit `app.py` on YOUR machine — change the message:**
```python
return "<h1>I changed this LIVE with volumes! 🔥</h1>"
```

**Step 5: Restart the container to see changes**
```bash
docker stop <container_id>
docker run -d -p 5000:5000 -v $(pwd):/app my-flask
```

**Step 6: Refresh browser** → You see the new message! 🎉

Without the volume, you'd have to `docker build` again every time you change code. With the volume, your local edits go straight into the container.

**Bonus: Enable auto-reload (no restart needed)**

Update `app.py` so Flask reloads automatically on file save:
```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

Rebuild once:
```bash
docker build -t my-flask .
docker run -d -p 5000:5000 -v $(pwd):/app my-flask
```

Now edit `app.py` → save → refresh browser → changes appear instantly! No restart needed.

---

### Volume Commands

```bash
# List all volumes
docker volume ls

# Inspect a volume (see where it's stored)
docker volume inspect mydata

# Remove a volume
docker volume rm mydata

# Remove ALL unused volumes (careful!)
docker volume prune
```

---

### Practical Example: PostgreSQL with Persistent Data

Without a volume — database data is lost when container stops:
```bash
docker run -d -e POSTGRES_PASSWORD=secret postgres:16
# Stop container → all your tables and data = gone 💀
```

With a volume — data survives:
```bash
docker run -d \
  -e POSTGRES_PASSWORD=secret \
  -v pg-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```

Now even if you stop and remove the container, your database data lives in the `pg-data` volume. Start a new container with the same volume → all your data is back.

---

### Quick Comparison

| | Named Volume | Bind Mount |
|--|--|--|
| Created by | Docker (`docker volume create`) | You (any folder on your PC) |
| Location | Docker manages it | You choose the path |
| Syntax | `-v myvolume:/app/data` | `-v /full/path:/app/data` |
| Best for | Databases, persistent storage | Development, sharing code |
| Portable | Yes | No (path is machine-specific) |

---

### Summary

```
Without volume:  Container dies → data dies 💀
With volume:     Container dies → data lives ✅
```

```bash
# Named volume (Docker manages storage)
docker run -v mydata:/app/data myimage

# Bind mount (your folder connected to container)
docker run -v $(pwd):/app myimage
```

---



### MultiStage Docker Build

- Multistage Docker build 
- Distroless


## Multistage Docker build 

Initially we have 

``` FROM ubuntu

RUN apt-get update && apt-get install -y python3 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY calculator.py .

<!--  Will take the Binary from here and than give to next making it stage 2-->

CMD ["python3", "calculator.py"] ```


# Stage 1
``` FROM ubuntu as Base

RUN apt-get update && apt-get install -y python3 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY calculator.py . ```

<!--  Will take the Artifact Binary from here and than give to next making it stage 2-->

```
From Python/java

copy --from Baseimage

CMD ["python3", "calculator.py"] ```

```



## Example of Frontent/Backend/Database full application with React and Java and Mysql

From ubuntu 

INstall dependemncies of java react and mysql

BUild java
Buikld frontend
EntryPoint [/app]


## After Multistaging

->Stage 1
From ubuntu as Build

INstall dependemncies of java react and mysql

BUild java
Buikld frontend

->Stage 2
From openjdk:11
copy --from BUild
EntryPoint [/app]



### Distroless Docker Image

It is basicaly a very minimialistic image with almost no dependency(ex openjdk 11)




