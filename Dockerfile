FROM ubuntu:22.04 AS base

RUN useradd -m -r osparcuser --uid 8004

USER root

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NOWARNINGS="yes"

RUN apt-get update --yes && apt-get upgrade --yes 
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install --yes --no-install-recommends python3 python-is-python3 python3-venv wget python3-pip gosu zip
RUN pip install uv

# Copying boot scripts                                                                                                                                                                                                                                                                                                   
COPY docker /docker

USER osparcuser

WORKDIR /home/osparcuser
RUN uv venv
RUN . .venv/bin/activate && uv pip install --upgrade -r /docker/requirements.txt 

USER root

ENTRYPOINT [ "/bin/bash", "-c", "/docker/entrypoint.bash" ]
