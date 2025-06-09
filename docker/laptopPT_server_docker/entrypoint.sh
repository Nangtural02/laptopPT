#!/bin/bash
set -e

# 기본값 처리
MYSQL_IP=${MYSQL_IP:-127.0.0.1}
FLASK_HOST=${FLASK_HOST:-127.0.0.1}
RUN_MANAGE=${RUN_MANAGE:-false}
INTERNAL_DOCKER_MYSQL=${INTERNAL_DOCKER_MYSQL:-false}

if [ "$INTERNAL_DOCKER_MYSQL" = "true" ]; then
  MYSQL_IP="host.docker.internal"
fi

ARGS="--mysql_ip $MYSQL_IP --host $FLASK_HOST"

if [ "$RUN_MANAGE" = "true" ]; then
  echo "🛠 DB 초기화 중..."
  python app.py $ARGS --manage
  echo "✅ DB 초기화 완료"
fi

echo "🚀 Flask 서버 실행..."
python app.py $ARGS
