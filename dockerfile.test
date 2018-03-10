FROM python:3.6.4-alpine
RUN pip install pipenv
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

FROM python:3.6.4-alpine
RUN pip install gunicorn
COPY --from=0 build/app /app/
WORKDIR /app
ENV PYTHONPATH /app/.venv/lib/python3.6/site-packages
ENTRYPOINT ["gunicorn"]
CMD ["flask_scratch.app:app"]