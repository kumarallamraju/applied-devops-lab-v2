# DevOps Internship Lab v2 — Jenkins + Groovy + Artifactory + SonarQube + TypeScript

✅ **Complete Working CI/CD Pipeline** featuring:
- Jenkins declarative pipeline with parallel stages (Groovy)
- Groovy shared library for reusable steps
- Python application: unit tests + tar.gz packaging
- TypeScript application: unit tests + TypeScript compilation + npm packaging
- SonarQube Community Edition: automated code quality scanning
- JFrog Artifactory OSS: artifact repository and storage
- Multi-language build orchestration on a single Jenkins instance

## Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Port availability: 8080 (Jenkins), 8081-8082 (Artifactory), 9000 (SonarQube)

### Launch Services
```bash
cd jenkins
docker compose up -d
```

This starts:
- **Jenkins** (with Python, Node.js, npm, SonarScanner pre-installed)
- **JFrog Artifactory** (generic artifact repository)
- **SonarQube** (Community Edition with PostgreSQL backend)

### Wait for Services to Be Ready
Services take 30-60 seconds to fully initialize. Check status:
```bash
docker compose ps
```

All containers should show "Up".

## Service URLs and Credentials

### Jenkins
- **URL**: http://localhost:8080
- **Username**: `admin`
- **Password**: (retrieve from container)
  ```bash
  docker exec -it devops-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
  ```

### JFrog Artifactory
- **UI**: http://localhost:8082/ui/
- **API**: http://localhost:8081/artifactory/
- **Username**: `admin`
- **Password**: `----`

### SonarQube
- **URL**: http://localhost:9000
- **Username**: `admin`
- **Password**: (set on first login; default is `admin` if not changed)

## Pipeline Overview

The Jenkins job (`devops-lab3`) executes a complete multi-stage pipeline:

### Stage 1: Checkout
- Clones the Git repository
- Loads the Groovy shared library (`local-shared-lib@main`)

### Stage 2: Quality (Parallel)

#### Python: Tests + Package
```groovy
stage('Python: tests + package') {
  - Create Python virtual environment
  - Install dependencies (pytest, package itself)
  - Run pytest
  - Package as tar.gz
  - Archive to dist/
}
```
**Output**: `app-python-0.1.X.tar.gz` (~7.6 MB)

#### TypeScript: Tests + Build + Package
```groovy
stage('TypeScript: tests/build/package') {
  - Run npm install
  - Execute Jest tests with coverage
  - Compile TypeScript (tsc)
  - Run npm pack
  - Archive to dist/
}
```
**Output**: `typescript-app-0.1.X.tgz` (~15 KB)

### Stage 3: SonarQube Scan
- Analyzes TypeScript source code (`src/` directory)
- Generates quality metrics in SonarQube dashboard
- Uses npm-based sonar-scanner (ARM64 compatible)

### Stage 4: Publish to Artifactory
- Uploads Python artifact to `example-repo-local/app-python-X.tar.gz`
- Uploads TypeScript artifact to `example-repo-local/typescript-app-X.tgz`
- Uses curl with HTTP PUT and basic auth

### Stage 5: Artifact Archive
- Jenkins archives all dist/* artifacts for build history

## Project Structure

```
├── Jenkinsfile                          # Pipeline definition (declarative)
├── README.md                            # This file
├── jenkins/
│   ├── Dockerfile                       # Custom Jenkins image with tools
│   ├── docker-compose.yml               # Service orchestration
├── groovy-shared-library/
│   ├── src/org/example/TextUtils.groovy # Utility functions
│   └── vars/
│       ├── dockerRun.groovy             # Docker step wrapper (archived)
│       └── sayHello.groovy              # Hello step
├── app-python/
│   ├── pyproject.toml                   # Python project config
│   ├── src/app_python/
│   │   ├── __init__.py
│   │   └── mathops.py                   # Math operations module
│   ├── tests/
│   │   └── test_mathops.py              # Unit tests (pytest)
│   └── tools/
│       └── uploader.py                  # Artifact upload utility
├── typescript-app/
│   ├── package.json                     # Node.js dependencies
│   ├── tsconfig.json                    # TypeScript compiler config
│   ├── jest.config.js                   # Jest test framework config
│   ├── sonar-project.properties         # SonarQube project settings
│   ├── src/
│   │   └── index.ts                     # TypeScript entry point
│   └── tests/
│       └── greet.test.ts                # Jest unit tests
└── docs/
    └── tutorial.md                      # Detailed setup guide
```

## Build Execution

### Running the Pipeline

1. Go to Jenkins: http://localhost:8080
2. Click on the `devops-lab3` job
3. Click **Build Now** (or wait for webhook trigger if configured)

### Monitoring

- Watch the build progress in the Jenkins UI
- View console output in real-time
- Artifacts are archived under **Build** > **Artifacts**

### Expected Build Output

```
[✓] Checkout — code pulled from GitHub
[✓] Python tests — 2 tests pass
[✓] Python package — 7.6 MB tar.gz created
[✓] TypeScript tests — 1 test passes
[✓] TypeScript build — dist/ compiled
[✓] TypeScript package — 15 KB tgz created
[✓] SonarQube scan — analysis uploaded to SonarQube
[✓] Artifactory upload — both artifacts stored
[✓] Build Success
```

## Verification

### Check Artifacts in Artifactory
```bash
curl -u admin:Azure12345678# http://localhost:8081/artifactory/api/search/artifact?name=app-python-*
curl -u admin:Azure12345678# http://localhost:8081/artifactory/api/search/artifact?name=typescript-app-*
```

### View SonarQube Results
- Open http://localhost:9000
- Project: `typescript-app`
- View metrics, issues, and code smells

### View Jenkins Artifacts
- Jenkins UI → `devops-lab3` → Build number → **Artifacts**
- Download archived tarballs

## Technology Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Jenkins | LTS (JDK 17) | CI/CD orchestration |
| Python | 3.11 | App runtime + tests |
| Node.js | 20 | TypeScript runtime |
| npm | 9.2 | Package manager |
| SonarScanner | 5.0.1 (npm) | Code quality analysis |
| SonarQube | Community | Quality metrics dashboard |
| PostgreSQL | 15 | SonarQube database |
| Artifactory | 7.71.5 OSS | Artifact repository |

## Customization

### Adding a New Build Stage
Edit `Jenkinsfile` and add a stage under `stages { ... }`:
```groovy
stage('Custom Step') {
  steps {
    sh 'echo "Your command here"'
  }
}
```

### Changing Artifact Paths
Modify the `ARTIFACTORY_REPO` environment variable in `Jenkinsfile`:
```groovy
environment {
  ARTIFACTORY_REPO = 'your-repo-name'
}
```

### Installing Additional Tools in Jenkins
Update `jenkins/Dockerfile`:
```dockerfile
RUN apt-get update && apt-get install -y <package-name>
```

Then rebuild:
```bash
docker compose build --no-cache jenkins
docker compose up -d
```

## Troubleshooting

### Services Not Starting
```bash
docker compose logs artifactory
docker compose logs sonarqube
docker compose logs jenkins
```

### SonarQube Analysis Fails
- Verify SonarQube is healthy: http://localhost:9000
- Check that sonar-token credential exists in Jenkins
- Ensure `sonar-scanner` is installed: `docker exec devops-jenkins which sonar-scanner`

### Artifactory Upload Fails
- Verify credentials in Jenkins: **Manage Credentials** > `artifactory-creds`
- Test connectivity: `curl -u admin:Azure12345678# http://localhost:8081/artifactory/api/repositories`
- Ensure target repository exists: `example-repo-local`

### Port Already in Use
If ports 8080, 8081, 9000 are in use, modify `jenkins/docker-compose.yml`:
```yaml
ports:
  - "8090:8080"  # Change host port
```

## Next Steps

- Review the Jenkinsfile to understand the pipeline stages
- Modify the Python or TypeScript apps and re-run the pipeline
- Add more test cases and see quality metrics update in SonarQube
- Extend the pipeline with deployment stages (e.g., Docker push, cloud deployment)

---

See `docs/tutorial.md` for detailed setup and troubleshooting steps.
