FROM jenkins/jenkins:lts-jdk17

USER root

# Install build tools (Python, Node.js, SonarScanner)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    unzip \
    curl \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Install sonar-scanner via npm
RUN npm install -g sonarqube-scanner

USER jenkins
