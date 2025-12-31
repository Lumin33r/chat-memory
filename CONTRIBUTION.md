# CONTRIBUTION.md

## Project: codeplatoon/practice/w12d2/lab

Welcome to the project! This guide will help you get started with development, Docker usage, Git workflow, and the steps to accomplish your assigned tasks.

---

## 1. Git Setup

### Initial Setup

1. Fork or clone the repository:
   ```bash
   git clone git@github.com:Lumin33r/codeplatoon.git
   cd codeplatoon/practice/w12d2/lab
   ```
2. Set your user info:
   ```bash
   git config user.name "Lumin33r"
   git config user.email "your_email@example.com"
   ```
3. Add the remote if not present:
   ```bash
   git remote add origin git@github.com:Lumin33r/codeplatoon.git
   ```

---

## 2. Daily Development Workflow

### Using Docker Containers

- Start containers:
  ```bash
  docker-compose up -d
  ```
- Attach to a running container:
  ```bash
  docker exec -it docker-session-lab-1 bash
  ```
- The project uses Docker volumes to persist data. Your code and data will be available even if you restart containers.

### When to Update Containers

- **Update the container** if you change dependencies (e.g., requirements.txt, Dockerfile) or need a new environment:
  ```bash
  docker-compose build
  docker-compose up -d --force-recreate
  ```
- **No need to rebuild** for pure Python code changes; just restart the app or container if needed.

### Git Commit Workflow

- Commit code changes frequently:
  ```bash
  git add .
  git commit -m "Describe your change"
  git push origin <branch>
  ```
- Pull latest changes before starting work:
  ```bash
  git pull origin main
  ```

---

## 3. Development Strategy for Assigned Tasks

### 1. Integrate with Flask

- Import and use your session store in the Flask app.
- Replace Flask's default session handling with your custom store.

### 2. Add User Authentication

- Implement user login/logout routes.
- Link session data to authenticated users (e.g., store user_id in session).

### 3. Implement Session Expiry

- Add timestamps to session data.
- Implement a cleanup routine (e.g., background job or on-access check) to remove expired sessions.

### 4. Add Redis Support

- Abstract session storage logic to support multiple backends.
- Implement a Redis backend using `redis-py`.
- Allow switching between file and Redis storage via config/env variable.

#### Suggested Steps

1. **Integrate session store with Flask** (test with local file backend).
2. **Implement user authentication** and link sessions to users.
3. **Add session expiry logic** and cleanup.
4. **Refactor to support Redis** as an alternative backend.
5. **Write tests** for all new features.
6. **Document** any new environment variables or setup steps in README.

---

## 4. Best Practices

- Use feature branches for new work.
- Write clear commit messages.
- Keep Docker containers running for development; rebuild only when dependencies change.
- Regularly push your work to remote.
- Ask for code reviews before merging to main.

---

Happy coding!
