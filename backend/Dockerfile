FROM python:3.6-alpine
LABEL maintainer="slawomir.zborowski@nokia.com"

ARG proxy
ENV http_proxy=$proxy https_proxy=$proxy

RUN pip3 install aiohttp==1.3.4 requests==2.18.4
ENV http_proxy= https_proxy=
ENTRYPOINT python3.6 /app/backend.py
