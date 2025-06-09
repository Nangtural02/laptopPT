FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x docker/laptopPT_server_docker/entrypoint.sh
ENTRYPOINT ["docker/laptopPT_server_docker/entrypoint.sh"]
