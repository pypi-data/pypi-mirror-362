PYTHON_3_8_DOCKERFILE_TEMPLATE = """FROM python:3.8
RUN apt-get update \
 && apt-get install -y ca-certificates \
 && rm -rf /var/lib/apt/lists/*
COPY ./ /tmp/
COPY fireware-https-proxy-ca.crt /usr/local/share/ca-certificates/fireware-https-proxy-ca.crt
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN useradd -u 9097 code_runner
USER code_runner:code_runner
WORKDIR /tmp
CMD ["bash", "-c", "python main.py > /tmp/logs/execution.log 2>&1"]
"""

PYTHON_3_9_DOCKERFILE_TEMPLATE = """FROM python:3.9
RUN apt-get update \
 && apt-get install -y ca-certificates \
 && rm -rf /var/lib/apt/lists/*
COPY ./ /tmp/
COPY fireware-https-proxy-ca.crt /usr/local/share/ca-certificates/fireware-https-proxy-ca.crt
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN useradd -u 9097 code_runner
USER code_runner:code_runner
WORKDIR /tmp
CMD ["bash", "-c", "python main.py > /tmp/logs/execution.log 2>&1"]
"""

PYTHON_3_10_DOCKERFILE_TEMPLATE = """FROM python:3.10
RUN apt-get update \
 && apt-get install -y ca-certificates \
 && rm -rf /var/lib/apt/lists/*
COPY ./ /tmp/
COPY fireware-https-proxy-ca.crt /usr/local/share/ca-certificates/fireware-https-proxy-ca.crt
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN useradd -u 9097 code_runner
USER code_runner:code_runner
WORKDIR /tmp
CMD ["bash", "-c", "python main.py > /tmp/logs/execution.log 2>&1"]
"""

PYTHON_3_11_DOCKERFILE_TEMPLATE = """FROM python:3.11
RUN apt-get update \
 && apt-get install -y ca-certificates \
 && rm -rf /var/lib/apt/lists/*
COPY ./ /tmp/
COPY fireware-https-proxy-ca.crt /usr/local/share/ca-certificates/fireware-https-proxy-ca.crt
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN useradd -u 9097 code_runner
USER code_runner:code_runner
WORKDIR /tmp
CMD ["bash", "-c", "python main.py > /tmp/logs/execution.log 2>&1"]
"""

PYTHON_3_12_DOCKERFILE_TEMPLATE = """FROM python:3.12
RUN apt-get update \
 && apt-get install -y ca-certificates \
 && rm -rf /var/lib/apt/lists/*
COPY ./ /tmp/
COPY fireware-https-proxy-ca.crt /usr/local/share/ca-certificates/fireware-https-proxy-ca.crt
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN useradd -u 9097 code_runner
USER code_runner:code_runner
WORKDIR /tmp
CMD ["bash", "-c", "python main.py > /tmp/logs/execution.log 2>&1"]
"""

NODE_24_DOCKERFILE_TEMPLATE = """FROM node:24
RUN apt-get update \
 && apt-get install -y ca-certificates \
 && rm -rf /var/lib/apt/lists/*
COPY ./ /tmp/
COPY fireware-https-proxy-ca.crt /usr/local/share/ca-certificates/fireware-https-proxy-ca.crt
RUN update-ca-certificates
RUN npm config set cafile /etc/ssl/certs/ca-certificates.crt
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
WORKDIR /tmp
RUN npm install --production --loglevel verbose
RUN useradd -u 9097 code_runner
USER code_runner:code_runner
CMD ["bash", "-c", "node main.js > /tmp/logs/execution.log 2>&1"]
"""