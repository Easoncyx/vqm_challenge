# FROM ubuntu:24.04
FROM nvidia/cuda:12.8.0-base-ubuntu24.04

ENV LANG=C.UTF-8
# setup timezone
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get -qq update && apt-get upgrade -y
RUN apt-get -y install --no-install-recommends \
    sudo \
    build-essential \
    nasm \
    git \
    python3.12 \
    python3.12-dev \
    python3.12-venv \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-tk 

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 2
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 2

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.6.6 /uv /uvx /bin/
# Install ffmpeg
COPY ./install_ffmpeg.sh .
RUN chmod +x ./install_ffmpeg.sh
RUN ./install_ffmpeg.sh

ADD . /vqm
WORKDIR "/vqm"
RUN uv sync --frozen

ENTRYPOINT ["uv","run","-m","vqm"]