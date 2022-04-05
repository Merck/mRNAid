FROM condaforge/miniforge3

RUN apt-get update -y \
        && apt-get install -y --no-install-recommends \
            libgtextutils-dev libtbb-dev \
            autoconf automake libcurl4-gnutls-dev libncurses5-dev \
            build-essential pkg-config \
        && apt-get -y clean && apt-get -y autoclean && apt-get -y autoremove

ENV PATH /opt/miniconda/bin:$PATH

RUN useradd docker
WORKDIR /backend

COPY ./flask_app/environment.yml ./flask_app/environment.yml

RUN conda env update -n base -f ./flask_app/environment.yml \
    && rm -rf /tmp/* \
    && conda clean --all

COPY . /backend
WORKDIR /backend/flask_app


CMD ["uwsgi", "--ini", "app.ini:uwsgi-docker"]
