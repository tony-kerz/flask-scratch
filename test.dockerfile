FROM feenix/python-build:3.6.4-alpine
ADD . /build
WORKDIR /build
RUN rm -rf .venv
RUN ls -la
ENV PIPENV_VENV_IN_PROJECT 1
RUN pipenv install
RUN mkdir app && \
    cp -r config app && \
    cp -r flask_scratch app && \
    cp -r .venv app && \
    cp __main__.py app
#RUN sed -i "1 s/.*/#\!\/app\/.venv\/bin\/python/" ./app/.venv/bin/gunicorn
RUN sed -i "1 s/.*/#\!.venv\/bin\/python/" ./app/.venv/bin/gunicorn


FROM python:3.6.4-alpine
COPY --from=0 build/app /app/
WORKDIR /app
#ENV PYTHONPATH /app/.venv/lib/python3.6/site-packages
ENV PATH /app/.venv/bin:$PATH
RUN echo $PATH
#ARG DEFAULT_GUNICORN_CMD_ARGS
#ENV GUNICORN_CMD_ARGS="$DEFAULT_GUNICORN_CMD_ARGS GUNICORN_CMD_ARGS"
#RUN echo "gunicorn-args=$GUNICORN_CMD_ARGS"
ENTRYPOINT ["gunicorn"]
CMD ["flask_scratch.app:app"]