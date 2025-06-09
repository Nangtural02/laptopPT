# 🐬 MySQL Docker Stack (`docker/mysql_server_docker`)

이 스택은 **독립형 MySQL 8** 컨테이너를 한 줄로 띄우고,
외부 IP `123.45.67.890:3306` (변경 가능)에 바로 노출하도록 구성되어 있습니다.

```text
mysql_server_docker/
├─ docker-compose.yml      # 서비스 정의
├─ conf.d/
│   └─ my.cnf              # bind-address = 0.0.0.0
└─ initdb/
    └─ init.sql            # DB·계정 자동 생성
```

## 1. 사전 준비

| 항목            | 기본값      | 비고                         |
| ------------- | -------- | -------------------------- |
| MySQL 루트 패스워드 | `rootpw` | `docker-compose.yml` 수정 가능 |
| 노출 포트         | `3306`   | 내부·외부 동일                   |

## 2. 실행

```bash
docker compose up -d         # 빌드 없이 바로 기동
docker compose down          # 중지
```

## 3. 접속 테스트

```bash
mysql -h 123.45.67.890 -P 3306 -u laptop_project_user -p
# default password: qwer1234. init.sql 파일에서 변경하세요.
```

## 4. 주요 폴더

| 폴더        | 용도                              |
| --------- | ------------------------------- |
| `conf.d/` | 추가 MySQL 설정(.cnf) 넣으면 자동 적용     |
| `initdb/` | 컨테이너가 **처음** 생길 때만 `.sql` 순차 실행 |

## 5. 흔한 문제

| 증상       | 해결                             |
| -------- | ------------------------------ |
| 외부 접속 불가 | 윈도우 방화벽/라우터에서 3306 인바운드 허용     |
| 인증 실패    | `init.sql` 수정 후 컨테이너 **새로** 생성 |

---