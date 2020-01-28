#!/bin/bash -e
#
# @author       Anthony Vilarim Caliani
# @contact      github.com/avcaliani
#

python_venv() {
  if [ ! -d ".venv" ]; then
    echo -e "\n\033[1;32m ¯\_(ツ)_/¯ \033[00m Creating Python VEnv...\n"
    python3 -m venv .venv \
      && source .venv/bin/activate \
      && pip install --upgrade pip \
      && pip install -r requirements.txt \
      && deactivate
  fi
}

echo -e "
     _   ___ ___ 
    /_\ | _ \_ _|
   / _ \|  _/| | 
  /_/ \_\_| |___| ENVIRONMENT
"

mkdir tmp || true

cd ../mr-owlf-mls/ \
  && ./start-dev.sh --package \
  && mv dist/mr_olwf_mls-*.tar.gz ../mr-owlf-api/tmp/ \
  && cd - \
  && python_venv \
  && source .venv/bin/activate \
  && pip install tmp/mr_olwf_mls-*.tar.gz \
  && deactivate \
  || exit 1

echo -e "\n\033[1;32m (งツ)ว \033[00m You are free to go!\n"
exit 0
