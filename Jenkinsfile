@Library('local-shared-lib@main') _

pipeline {
  agent any

  environment {
    VERSION = "0.1.${env.BUILD_NUMBER}"

    // docker-compose sets project name: devops-lab => network: devops-lab_default
    DOCKER_NETWORK = 'devops-lab_default'

    ARTIFACTORY_BASE_URL = 'http://artifactory:8081/artifactory'
    ARTIFACTORY_REPO = 'generic-local'

    SONAR_HOST_URL = 'http://sonarqube:9000'

    PY_ARTIFACT = "app-python-${VERSION}.tar.gz"
  }

  // timestamps() requires the Timestamper plugin; removed for compatibility

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        sayHello(name: 'Applied DevOps Lab v2')
        sh 'mkdir -p dist'
      }
    }

    stage('Quality (Parallel)') {
      parallel {
        stage('Python: tests + package') {
          steps {
            dockerRun(
              image: 'python:3.11-slim',
              workdir: '/app',
              mounts: ["${env.WORKSPACE}/app-python:/app", "${env.WORKSPACE}/dist:/dist"],
              cmd: """
                python -m pip install -U pip >/dev/null
                pip install -e . pytest >/dev/null
                pytest -q
                cd / && tar -czf /dist/${PY_ARTIFACT} -C /app .
                ls -lh /dist
              """
            )
          }
        }

        stage('TypeScript: tests/build/package') {
          steps {
            dockerRun(
              image: 'node:20-bullseye',
              workdir: '/app',
              mounts: ["${env.WORKSPACE}/typescript-app:/app", "${env.WORKSPACE}/dist:/app/../dist"],
              cmd: """
                bash scripts/package.sh
                ls -lh ../dist
              """
            )
          }
        }
      }
    }

    stage('SonarQube Scan (TypeScript)') {
      steps {
        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
          dockerRun(
            image: 'sonarsource/sonar-scanner-cli:latest',
            workdir: '/src',
            network: "${DOCKER_NETWORK}",
            mounts: ["${env.WORKSPACE}/typescript-app:/src"],
            cmd: """
              sonar-scanner \
                -Dsonar.host.url=${SONAR_HOST_URL} \
                -Dsonar.token=${SONAR_TOKEN}
            """
          )
        }
      }
    }

    stage('Publish to Artifactory') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'artifactory-creds', usernameVariable: 'ART_USER', passwordVariable: 'ART_PASS')]) {
          dockerRun(
            image: 'python:3.11-slim',
            workdir: '/w',
            network: "${DOCKER_NETWORK}",
            mounts: ["${env.WORKSPACE}:/w"],
            cmd: """
              python /w/app-python/tools/uploader.py \
                --base-url ${ARTIFACTORY_BASE_URL} \
                --repo ${ARTIFACTORY_REPO} \
                --file /w/dist/${PY_ARTIFACT} \
                --target-path app-python/${VERSION}/${PY_ARTIFACT} \
                --username ${ART_USER} --password ${ART_PASS}

              TS_FILE=\$(ls /w/dist/typescript-app-*.tgz | head -n 1)
              python /w/app-python/tools/uploader.py \
                --base-url ${ARTIFACTORY_BASE_URL} \
                --repo ${ARTIFACTORY_REPO} \
                --file ${TS_FILE} \
                --target-path typescript-app/${VERSION}/\$(basename ${TS_FILE}) \
                --username ${ART_USER} --password ${ART_PASS}
            """
          )
        }
      }
    }
  }

  post {
    always { archiveArtifacts artifacts: 'dist/*', fingerprint: true }
  }
}
