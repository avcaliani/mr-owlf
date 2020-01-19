#!/bin/bash
# @author       Anthony Vilarim Caliani
# @contact      github.com/avcaliani


echo -e  "
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
     > Data Stream Service <
"

if [ ! -d ".venv" ]; then
    echo -e "\n\033[1;32m ¯\_(ツ)_/¯ \033[00m Creating Python VEnv...\n"
    python3 -m venv .venv \
      && source .venv/bin/activate \
      && pip install --upgrade pip \
      && pip install -r requirements.txt \
      && deactivate
fi

export APP_LOG_LEVEL="DEBUG"
source .venv/bin/activate && python mr_owlf_dss/main.py "$@" && deactivate
unset $APP_LOG_LEVEL

echo -e "\n\033[1;32m (งツ)ว \033[00m You nailed it!\n"
exit 0
