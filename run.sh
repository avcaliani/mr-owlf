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
  echo -e "\033[0;31mERROR\033[00m  $1"
}

build_image() {
  cd "./$1" && docker build -f DockerFile -t "$1" . && cd ..
}


  # # #    #   #    #   #    #   #    # # #    #   #    # # #
  #   #    #   #    ##  #    ##  #      #      ##  #    #
  # #      #   #    # # #    # # #      #      # # #    #  ##
  #  #     #   #    #  ##    #  ##      #      #  ##    #   #
  #   #    # # #    #   #    #   #    # # #    #   #    # # #


echo -e  "
      __________
     / ___  ___ \\
    / / @ \\/ @ \\ \\
    \\ \\___/\\___/ /\\
     \\____\\/____/||
     /     /\\\\\\\\\\\\\\\\\\//
     |     |\\\\\\\\\\\\\\\\\\\\\\\\
      \\      \\\\\\\\\\\\\\\\\\\\\\\\
       \\______/\\\\\\\\\\\\\\\\
        _||_||_
         -- --
        \033[1;33mMr. Owlf\033[00m
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
    build_image "mr-owlf-dss"
    build_image "mr-owlf-mls"
    docker-compose up -d
    ;;

  stop)
    cool "Cleaning things up..."
    docker-compose stop
    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)
    ;;

  -h)
    info "  Available Commands:"
    info "   - start       : Start Application"
    info "   - stop        : Stop Application"
    ;;

  *)
    error "Invalid option '$1'..."
    info "See available options running with \"-h\" flag :)"
    ;;

esac

info "Bye!"
exit 0
