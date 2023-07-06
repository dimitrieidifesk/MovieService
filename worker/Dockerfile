FROM python:3.10

WORKDIR /opt/worker

RUN apt-get update && apt-get install -y \
     python3-dev  \
     netcat-traditional \
     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x /opt/worker/run_parser.sh
ENTRYPOINT [ "/opt/worker/run_parser.sh" ]