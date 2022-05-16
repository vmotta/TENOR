#Using EC2 AWS Ubuntu 18.04 LTS (t2.micro)

#Installing nodejs

# Pull base image.
FROM ubuntu:16.04

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
CMD ["/usr/sbin/sshd", "-D"]

COPY things/*.js /home/ubuntu/thingweb.node-wot/examples/scripts/

VOLUME thingweb

WORKDIR /home/ubuntu/thingweb.node-wot/

EXPOSE 8080 22