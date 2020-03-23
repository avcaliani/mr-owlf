# 🤖 Mr. Owlf Machine Learning Service
By Anthony Vilarim Caliani

[![#](https://img.shields.io/badge/licence-MIT-lightseagreen.svg)](#) [![#](https://img.shields.io/badge/python-3.7.x-yellow.svg)](#)

## Running Locally

> **Before running** make sure that you have prepared your "MongoDB" instance. This may help you 👉 [docker-compose](../mongodb/docker-compose.yml)

```bash
# That's all buddy...
./start-dev.sh
```

## Running Sample

```bash
# IMPORTANT 
# ----------
# Before running this sample you must have been executed "./start-dev.sh" at least once
# to generate "classifier.pkl" and "vectorizer.pkl" files
./start-dev.sh --sample
```

## Packaging

```bash
./start-dev.sh --package
```

## Running on Docker
```bash
# Creating Docker Image
docker build -f DockerFile -t mr-owlf-mls .

# Creating Docker Container
docker run -d --network host --name mr-owlf-mls mr-owlf-mls

# Looking for logs
docker logs mr-owlf-mls
```
