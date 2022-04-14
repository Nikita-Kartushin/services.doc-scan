FROM python:3.8

USER root

ARG SSH_PRIVATE_KEY

RUN mkdir -p /root/.ssh/ && \
    mkdir -p /var/www/services.doc-scan/logs && \
    mkdir -p /var/www/services.doc-scan/tmp

# Add SSH key
RUN mkdir -p /root/.ssh/ && \
    echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa && \
    touch touch /root/.ssh/known_hosts && \
    chmod 600 /root/.ssh/id_rsa && \
    ssh-keyscan ... >> /root/.ssh/known_hosts && \
    mkdir /install

# Install packages

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
 apt-get update && \
 apt-get install -y nginx libgl1-mesa-glx tesseract-ocr nodejs && \
 npm install apidoc -g

# Install requirements
WORKDIR /tmp

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt && rm requirements.txt

# Copy files

WORKDIR /var/www/services.doc-scan

COPY app ./
COPY apidoc.json ./apidoc.json
COPY entrypoint.sh ./entrypoint.sh
COPY rus.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
COPY services.doc-scan.nginx.conf /etc/nginx/sites-enabled/services.doc-scan.conf

# RUN
RUN chmod -R 777 /var/www && apidoc -i . -o ../documentation/

EXPOSE 6060
CMD ["bash", "entrypoint.sh"]