# 🚀 Flask Server Docker (`docker/laptopPT_server_docker`)

Flask 앱을 **컨테이너 한 개**로 실행합니다. MySQL 주소·호스트 바인딩·DB 초기화 여부를 **.env** 한 곳에서 관리합니다.

```text
laptopPT_server_docker/
├─ Dockerfile
├─ docker-compose.yml
├─ entrypoint.sh
└─ .env                # 실행 옵션
```

## 1. .env 설정

```env
MYSQL_IP=123.45.67.890        # MySQL 서버 IP
FLASK_HOST=0.0.0.0             # 0.0.0.0 = 컨테이너 외부에서 접속, 127.0.0.1 = 컨테이너의 로컬전용
INTERNAL_DOCKER_MYSQL=false    # 동일 pc의 docker에서 MySQL 서버 구동 시 true.
RUN_MANAGE=true                # csv로 DB 초기화하는 작업을 컨테이너 시작 시 적용할 지 여부.
```

> 첫 실행 후 **RUN\_MANAGE=false** 로 바꿔두고 재기동하면 DB 서버 초기화 없이 바로 서버가 실행됩니다.

## 2. 실행

```bash
# 초기화 + 서버
cd docker/laptopPT_server_docker
docker compose up --build -d

# 이후 서버만 (RUN_MANAGE=false로 바꾼 뒤)
docker compose up -d
```

## 3. 커스텀 환경변수

| 변수                      | 설명                                   |
| ----------------------- | ------------------------------------ |
| `MYSQL_IP`              | MySQL 서버 주소                          |
| `FLASK_HOST`            | Flask `app.run()` 호스트 주소             |
| `INTERNAL_DOCKER_MYSQL` | true면 `host.docker.internal` 사용      |
| `RUN_MANAGE`            | true면 `python app.py --manage` 1회 실행 |

## 4. 흔한 문제

| 증상                        | 해결                               |
| ------------------------- |----------------------------------|
| `Table ... doesn't exist` | `.env`에서 `RUN_MANAGE=true` 후 재빌드 |
| 외부 접속 불가                  | 방화벽·NAT 8080 포트 개방               |
| MySQL 연결 실패               | `.env` IP·방화벽·INTERNAL 옵션 확인     |

---

## 배포 팁

1. 루트 커밋에 `docker/` 폴더만 포함해도 다른 개발자가 `docker compose up` 한 줄로 전체 스택 실행 가능.
2. `.env`는 민감 정보 포함되므로 `.env.example` 샘플만 커밋하고 실제 `.env`는 깃 ignore.
3. GitHub Actions로 `docker build` + `docker push` 자동화 가능.
