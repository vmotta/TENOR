#FROM python:3.8-slim-buster
#WORKDIR /app
# We copy just the requirements.txt first to leverage Docker cache
#COPY ./requirements.txt /app/requirements.txt
#RUN pip install -r requirements.txt
#COPY . /app
#EXPOSE 8080 5000
#CMD ["python", "/app/app.py"]

# syntax=docker/dockerfile:1
FROM python:3.7-slim-buster

RUN apt-get update

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
#RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080 5000
#CMD [ "flask", "run" ]

WORKDIR /home/ubuntu

RUN apt-get install -y curl

RUN curl -sL https://deb.nodesource.com/setup_12.x -o nodesource_setup.sh

RUN bash nodesource_setup.sh

RUN apt install -y nodejs

RUN apt install -y build-essential

RUN apt install -y vim

#Provinding Thingweb project

RUN apt install -y git

RUN git clone https://github.com/eclipse/thingweb.node-wot

WORKDIR /home/ubuntu/thingweb.node-wot 

RUN npm install -g npm@7

RUN npm install typescript -g

RUN npm install @types/node --save-dev

RUN npm run build

RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:mypassword' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

COPY things/*.js /home/ubuntu/thingweb.node-wot/examples/scripts/

VOLUME thingweb

WORKDIR /home/ubuntu/thingweb.node-wot/

WORKDIR /app

CMD python3 -m flask run --host=0.0.0.0 && /usr/sbin/sshd -D