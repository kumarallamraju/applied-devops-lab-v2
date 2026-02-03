FROM jenkins/jenkins:lts-jdk17

USER root

# Install Docker CLI
RUN curl -fsSL https://get.docker.com | sh \
  && usermod -aG docker jenkins

USER jenkins
