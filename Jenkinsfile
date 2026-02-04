@Library('local-shared-lib@main') _

pipeline {
  agent any

  environment {
    VERSION = "0.1.${env.BUILD_NUMBER}"

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
            dir('app-python') {
              sh 'python3 -m pip install -U pip'
              sh 'python3 -m pip install -e . pytest'
              sh 'pytest -q'
              sh "tar -czf ../dist/${PY_ARTIFACT} -C . ."
              sh 'ls -lh ../dist'
            }
          }
        }

        stage('TypeScript: tests/build/package') {
          steps {
            dir('typescript-app') {
              sh 'npm install'
              sh 'npm test -- --coverage'
              sh 'npm run build'
              sh 'npm pack'
              sh 'mkdir -p ../dist'
              sh 'mv typescript-app-*.tgz ../dist/'
              sh 'ls -lh ../dist'
            }
          }
        }
      }
    }

    stage('SonarQube Scan (TypeScript)') {
      steps {
        withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
          dir('typescript-app') {
            sh """
              sonar-scanner \
                -Dsonar.projectKey=typescript-app \
                -Dsonar.sources=src \
                -Dsonar.host.url=${SONAR_HOST_URL} \
                -Dsonar.token=${SONAR_TOKEN}
            """
          }
        }
      }
    }

    stage('Publish to Artifactory') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'artifactory-creds', usernameVariable: 'ART_USER', passwordVariable: 'ART_PASS')]) {
          sh """
            python3 app-python/tools/uploader.py \
              --base-url ${ARTIFACTORY_BASE_URL} \
              --repo ${ARTIFACTORY_REPO} \
              --file dist/${PY_ARTIFACT} \
              --target-path app-python/${VERSION}/${PY_ARTIFACT} \
              --username ${ART_USER} --password ${ART_PASS}

            TS_FILE=\$(ls dist/typescript-app-*.tgz | head -n 1)
            python3 app-python/tools/uploader.py \
              --base-url ${ARTIFACTORY_BASE_URL} \
              --repo ${ARTIFACTORY_REPO} \
              --file \$TS_FILE \
              --target-path typescript-app/${VERSION}/\$(basename \$TS_FILE) \
              --username ${ART_USER} --password ${ART_PASS}
          """
        }
      }
    }
  }

  post {
    always { archiveArtifacts artifacts: 'dist/*', fingerprint: true }
  }
}
