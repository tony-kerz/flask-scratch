#FROM python:3.6.4-slim-stretch
#FROM python:3.6.4-alpine3.7
# from frolvlad/alpine-python3
FROM feenix/python-build:3.6.4
#FROM feenix/python-ml-build:3.6.4

ARG package
ENV package=${package}
ENV PIPENV_VENV_IN_PROJECT 1

ADD . /build
WORKDIR /build

RUN \
#    time apk --update add build-base &&\
    #apt-get update &&\
    #apt-get install -y time &&\
    #time apt-get install -y build-essential &&\
#   time pip install pipenv &&\
    rm -rf .venv &&\
    date &&\
    time pipenv install &&\
    date &&\
    mkdir app && \
    cp -r config app && \
    cp -r ${package} app && \
    cp -r .venv app && \
    cp __main__.py app &&\
    sed -i "1 s/.*/#\!.venv\/bin\/python/" ./app/.venv/bin/gunicorn

#FROM python:3.6.4-slim
#FROM python:3.6.4-slim-stretch
#FROM frolvlad/alpine-python3
FROM feenix/python:3.6.4
#FROM feenix/python-ml:3.6.4

ARG package
ENV package=${package}

COPY --from=0 build/app /app/
WORKDIR /app
#RUN ls -la && cat .venv/bin/gunicorn
#RUN ls -laR
ENV PYTHONPATH /app/.venv/lib/python3.6/site-packages
ENV PATH /app/.venv/bin:$PATH
ARG gunicorn_cmd_args=--bind=0.0.0.0:8000
ENV GUNICORN_CMD_ARGS=${gunicorn_cmd_args}

ARG cmd=gunicorn
ENV cmd=${cmd}

# real ENTRYPOINT not working well with env vars, so jamming into CMD
# ENTRYPOINT ["gunicorn"]
#ENV entrypoint=.
ENV entrypoint=${package}.app:app

CMD ${cmd} ${entrypoint}