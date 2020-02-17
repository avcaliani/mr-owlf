# 🌎 Mr. Owlf API
By Anthony Vilarim Caliani

[![#](https://img.shields.io/badge/licence-MIT-lightseagreen.svg)](#) [![#](https://img.shields.io/badge/python-3.7.x-yellow.svg)](#)

## Running Locally

> **Before running** make sure that you have prepared your "MongoDB" instance. This may help you 👉 [docker-compose](../mongodb/docker-compose.yml)

```bash
# IMPORTANT 
# ----------
# The "init-env.sh" script is very important because it will create our python "venv" and install
# all dependencies listed on "requirements.txt" file, but this script will also create
# "mr-owlf-mls" package and install it, by the way this dependency is mandatory as well.

# Creating our development environment
./init-env.sh

# Running our API locally \o/
source .venv/bin/activate && python app/main.py && deactivate
```

## Running on Docker
```bash
# Creating Docker Image
docker build -f DockerFile -t mr-owlf-api .

# Creating Docker Container
docker run -d \
	--mount source=tmp,target=/tmp \
	-p 80:80 \
	--name mr-owlf-api \
	mr-owlf-api
```

## Creating PKL files
To create `classifier.pkl` and `vectorizer.pkl` files you must execute [mr-owlf-mls](../mr-owlf-mls/README.md) project, and then copy all generated `*.pkl` files to `./.dev/`, after that you will be ready to go.

## API Usage
```bash
# Get statistics
curl localhost:8080/statistic

# Processing some data...
curl -d '{ 
			"sentence": "A Wikipedia anunciou que será forçada a retirar a inscrição para Ostrich devido à falta de financiamento",
			"author": "dwaxe", 
			"domain": "news.clickhole.com", 
			"publish_date": "2019-08-10"
	}' \
     -H 'Content-Type: application/json' \
     -X POST http://localhost:8080/score


```

---

_You can find [@avcaliani](#) at [GitHub](https://github.com/avcaliani) or [GitLab](https://gitlab.com/avcaliani)._