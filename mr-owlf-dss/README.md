# 📦 Mr. Owlf Data Stream Service
By Anthony Vilarim Caliani

[![#](https://img.shields.io/badge/licence-MIT-lightseagreen.svg)](#) [![#](https://img.shields.io/badge/python-3.7.x-yellow.svg)](#)

## Running Locally

> **Before running** make sure that you have prepared your "MongoDB" instance. This may help you 👉 [docker-compose](../mongodb/docker-compose.yml)

```bash
# That's all buddy...
./start-dev.sh
```

## Running on Docker
```bash
# Creating Docker Image
docker build -f DockerFile -t mr-owlf-dss .

# Creating Docker Container
docker run -d --network host --name mr-owlf-dss mr-owlf-dss

# Looking for logs
docker logs mr-owlf-dss
```

---

_You can find [@avcaliani](#) at [GitHub](https://github.com/avcaliani) or [GitLab](https://gitlab.com/avcaliani)._

