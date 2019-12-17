FROM python:3.8.0-buster

LABEL maintainer="Clovis Chanay <clovis.chanay@outlook.com>"

ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./ /project
WORKDIR /project

CMD ["bash", "entrypoint.sh"]
