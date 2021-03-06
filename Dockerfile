# Main image
FROM docker.io/library/python:3.10.5

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    XDG_CONFIG_HOME=/config

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
RUN python -m pip install --no-cache-dir --use-feature=in-tree-build .

CMD ["kopf", "run", "--liveness=http://0.0.0.0:8080/healthz", "-m", "dnsrpzrecord-controller"]
