#!/bin/bash
# @author       Anthony Vilarim Caliani
# @contact      github.com/avcaliani
#
# @Description
# Mr. Owlf application runner.


  # # #    #   #    #   #    # # #    # # #    # # #    # # #    #   #    # # #
  #        #   #    ##  #    #          #        #      #   #    ##  #    #
  # #      #   #    # # #    #          #        #      #   #    # # #    # # #
  #        #   #    #  ##    #          #        #      #   #    #  ##        #
  #        # # #    #   #    # # #      #      # # #    # # #    #   #    # # #


cool() {
  echo -e "\033[1;32m(งツ)ว \033[00m$1"
}

info() {
  echo -e "\033[1;34mINFO\033[00m   $1"
}

error() {
  echo -e "\033[1;31mERROR\033[00m  $1"
}

build_image() {
  if [[ "$(docker images -q $1 2> /dev/null)" == "" ]]; then
    cd "./$1" && docker build -f DockerFile -t "$1" . && cd -
  else
    echo "Image '$1' already exists!"
  fi
}


  # # #    #   #    #   #    #   #    # # #    #   #    # # #
  #   #    #   #    ##  #    ##  #      #      ##  #    #
  # #      #   #    # # #    # # #      #      # # #    #  ##
  #  #     #   #    #  ##    #  ##      #      #  ##    #   #
  #   #    # # #    #   #    #   #    # # #    #   #    # # #


echo -e  "
   __  __         ___         _  __ 
  |  \/  |_ _    / _ \__ __ _| |/ _|
  | |\/| | '_|  | (_) \ V  V / |  _|
  |_|  |_|_|(_)  \___/ \_/\_/|_|_|  
"

if [ -z $(command -v docker) ]; then
  error "Docker is not installed, please try to install it first."
  exit 1
fi

if [ -z $(command -v docker-compose) ]; then
  error "docker-compose is not installed, please try to install it first."
  exit 1
fi

case "$1" in
  start)
    cool "Starting project..."
    cd mr-owlf-api && ./init-env.sh && cd -
    build_image "mr-owlf-dss"
    build_image "mr-owlf-mls"
    build_image "mr-owlf-api"
    build_image "mr-owlf-front"
    docker-compose up -d
    ;;

  stop)
    cool "Cleaning things up..."
    docker-compose down
    ;;

  -h)
    info "[ AVAILABLE COMMANDS ]"
    info " -h    : Help"
    info " start : Start Application"
    info " stop  : Stop Application"
    ;;

  *)
    error "Invalid option '$1'..."
    info "See available options running with \"-h\" flag :)"
    ;;
esac

info "Bye!"
exit 0
