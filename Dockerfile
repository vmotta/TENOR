# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /home/ubuntu

RUN apt-get update

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

EXPOSE 8080 22

#CMD ["/usr/sbin/sshd", "-D"]

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

CMD /usr/sbin/sshd -D  && python3 -m flask run --host=0.0.0.0