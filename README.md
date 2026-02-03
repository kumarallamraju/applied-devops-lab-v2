# DevOps Internship Lab v2 — Jenkins + Groovy + Artifactory + SonarQube + TypeScript

✅ What you can practice locally:
- Jenkins declarative pipeline (Groovy)
- Groovy shared library
- JFrog Artifactory OSS (artifact upload)
- SonarQube Community (code scan)
- TypeScript build + tests + package
- Python tests + artifact + upload automation

## Start
```bash
cd jenkins
docker compose up -d
```

## Service URLs and Login Details

**Jenkins**
- URL: http://localhost:8080
- Username: `admin`
- Initial password:
	```bash
	docker exec -it devops-jenkins cat /var/jenkins_home/secrets/initialAdminPassword
	```

**JFrog Artifactory OSS**
- UI: http://localhost:8082/ui/
- API: http://localhost:8081/artifactory/
- Username: `admin`
- Password: `password` (you will be prompted to change it on first login)

**SonarQube Community**
- URL: http://localhost:9000
- Username: `admin`
- Password: `admin` (you will be prompted to change it on first login)

Open `docs/tutorial.md` for setup steps.
