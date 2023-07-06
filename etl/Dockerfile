FROM python:3.10

WORKDIR /opt/etl

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT [ "python","main.py" ]