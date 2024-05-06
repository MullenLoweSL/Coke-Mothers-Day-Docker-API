# https://github.com/Azure/azure-functions-docker
# https://hub.docker.com/_/microsoft-azure-functions-base
FROM mcr.microsoft.com/azure-functions/python:3.0-python3.7

ENV AzureWebJobsScriptRoot=/home/site/wwwroot
ENV AzureFunctionsJobHost__Logging__Console__IsEnabled=true
ENV DEBIAN_FRONTEND noninteractive

COPY . /home/site/wwwroot

# install LibreOffice
RUN mkdir -p /usr/share/man/man1
RUN apt-get update --allow-releaseinfo-change && \
    apt-get -y -q install \
		ffmpeg

RUN /usr/bin/ffmpeg -version

RUN cd /home/site/wwwroot && pip install -r requirements.txt