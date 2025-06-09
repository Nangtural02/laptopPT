#!/bin/bash
set -e

MYSQL_IP=${MYSQL_IP:-127.0.0.1}
FLASK_HOST=${FLASK_HOST:-127.0.0.1}
RUN_MANAGE=${RUN_MANAGE:-false}

# 옵션이 **존재**하고 값이 true/TRUE/1 일 때만 내부 게이트웨이 사용
if [[ -n "$INTERNAL_DOCKER_MYSQL" ]] && [[ "${INTERNAL_DOCKER_MYSQL,,}" =~ ^(true|1)$ ]]; then
  MYSQL_IP="host.docker.internal"
fi

ARGS="--mysql_ip $MYSQL_IP --host $FLASK_HOST"

if [[ "${RUN_MANAGE,,}" =~ ^(true|1)$ ]]; then
  echo "🛠  DB 초기화 중..."
  python app.py $ARGS --manage
  echo "✅ DB 초기화 완료"
fi

echo "🚀 Flask 서버 실행..."
exec python app.py $ARGS
