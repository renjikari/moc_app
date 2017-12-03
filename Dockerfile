FROM ubuntu:latest
LABEL maintainer "@renjikari"
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev build-essential libmysqlclient-dev
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
