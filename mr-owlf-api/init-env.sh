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
          __________
         / ___  ___ \\
        / / \033[1;32m@\033[00m \\/ \033[1;32m@\033[00m \\ \\
        \\ \\___/\\___/ /\\
         \\____\\/____/||
         /     /\\\\\\\\\\\\\\\\\\//
         |     |\\\\\\\\\\\\\\\\\\\\\\\\
          \\      \\\\\\\\\\\\\\\\\\\\\\\\
           \\______/\\\\\\\\\\\\\\\\
            _||_||_
             -- --
            \033[1;32mMr. Owlf\033[00m
      > Environment Setup <
"

mkdir .dev || true

cd ../mr-owlf-mls/ \
  && python_venv \
  && source .venv/bin/activate \
  && python setup.py sdist \
  && deactivate \
  && mv dist/mr_olwf_mls-*.tar.gz ../mr-owlf-api/.dev/ \
  && cd - \
  && python_venv \
  && source .venv/bin/activate \
  && pip install .dev/mr_olwf_mls-*.tar.gz \
  && deactivate \
  || exit 0

echo -e "\n\033[1;32m (งツ)ว \033[00m You are free to go!\n"
exit 1
