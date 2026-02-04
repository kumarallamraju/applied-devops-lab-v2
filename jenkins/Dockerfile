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

RUN curl -fsSL https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip -o /tmp/sonar-scanner.zip \
  && unzip /tmp/sonar-scanner.zip -d /opt \
  && ln -s /opt/sonar-scanner-5.0.1.3006-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner \
  && rm /tmp/sonar-scanner.zip

USER jenkins
