FROM python:3.9
MAINTAINER Danielle Stacy "dastacy@cisco.com"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENV FLASK_ENV development
ENV FLASK_APP src

RUN flask init-db
EXPOSE 5000
CMD flask run --host 0.0.0.0
