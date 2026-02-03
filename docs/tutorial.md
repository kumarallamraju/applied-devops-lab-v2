# Setup & Practice (v2)

## 1) Start services
```bash
cd jenkins
docker compose up -d
```

## 2) Jenkins setup
1) Install plugins: Pipeline, Git, Credentials Binding
2) Add credentials:
- `artifactory-creds` (username/password)
- `sonar-token` (secret text)
3) Configure shared library:
- Manage Jenkins → System → Global Pipeline Libraries
- Name: `local-shared-lib`
- Repo: this repo
- Library path: `groovy-shared-library`

## 3) SonarQube token
- Open http://localhost:9000
- Login `admin/admin` → change password
- My Account → Security → Generate token
- Save into Jenkins credential `sonar-token`

## 4) Artifactory repo
If `generic-local` is missing:
- Artifactory → Administration → Repositories → Local → New → Generic → `generic-local`

## 5) Run pipeline
Create a Jenkins Pipeline job pointing to this repo with Script Path `Jenkinsfile`.

## Exercises
- Add eslint lint stage
- Add manual approval before publish
- Add Sonar quality gate check
