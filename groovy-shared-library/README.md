# Groovy Shared Library

Register in Jenkins:
- Manage Jenkins → System → Global Pipeline Libraries
- Name: `local-shared-lib`
- Retrieval: Git
- Library path: `groovy-shared-library`

Steps:
- `sayHello(name: ...)`
- `dockerRun(image: ..., cmd: ..., mounts: [...], workdir: ..., network: ...)`
