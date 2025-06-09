# 🖥️ 노트북 견적좀짜줘 너 컴공이잖아 (LaptopPT)

간단한 질문 혹은 세부 조건을 통해 예산·성능·편의 기능을 종합적으로 비교하고
가격·재고·성능 정보를 한눈에 확인할 수 있는 Flask + MySQL 기반 웹 서비스입니다.

---

## 📌 주요 기능

1. **프리셋(기초) 검색**

   * 예산, 용도, 휴대성 선택만으로 추천 성능 범위 자동 설정
   * CPU PassMark / GPU 3DMark 기반으로 후보 노트북 추출

2. **상세 검색**

   * 예산 범위 · CPU/GPU 성능 범위 · 디스플레이 크기 · RAM · 저장장치 · 해상도 등
   * HDMI, SD 슬롯, LAN 포트, PD 충전, 썬더볼트 등 편의 기능 필터링

3. **검색 결과 & 조건 수정**

   * noUiSlider 슬라이더 UI로 직관적 조건 조정
   * 재검색 시 이전 입력값 그대로 유지
   * 결과 항목별 “🔍 상세 보기” 버튼으로 클릭 한 번에 세부 페이지 이동

4. **노트북 상세 페이지**

   * CPU/GPU 모델명·벤치마크 점수
   * RAM·저장장치 옵션, 디스플레이·전력·무게·배터리
   * 실시간 판매처별 가격·품절 여부
   * **가격 추이 차트** (Chart.js)
   * **사용자 리뷰** (별점·코멘트)

---

## 🛠️ 기술 스택

* **Python 3.12**
* **Flask 2.3**
* **MySQL 8.0** 
* **SQLAlchemy 2.0** ORM
* Jinja2 템플릿 + **Tailwind CSS** + **noUiSlider**, **Chart.js**
* 데이터 수집: CSV → MySQL Seed 스크립트

---

## 🛠️ 설치 & 실행(Windows로컬)

> **전제**: 이미 실행 중인 **MySQL 8** 서버가 있으며 접속 계정은 `laptop_project_user/qwe123`, DB `laptopPT`가 준비돼 있다고 가정합니다.   
> (Docker로 mysql서버 실행/Docker에서 웹서버 구동은 맨 아래 "🐳 Docker 실행" 참고)  

1. 터미널(git bash, windows powershell, mac terminal 등)에서 다음을 실행하세요.    
예시로 넣은 ip 주소인 123.45.67.890은 본인 PC의 주소에 맞게 변경하세요. 잘 모르시겠으면 우선 local로 구동해보세요.

```bash
# 1) 소스 내려받기
git clone https://github.com/Nangtural02/laptopPT.git
cd laptopPT

# 2) 파이썬 의존성 설치
pip install -r requirements.txt

# 3) DB 초기화(최초 1회만)
python app.py --mysql_ip 123.45.67.890 --host local --manage

# 4) 웹 서버 실행
python app.py --mysql_ip 123.45.67.890 --host local          # localhost 전용
# 외부 노출하려면
python app.py --mysql_ip 123.45.67.890 --host 123.45.67.890 
```

2. **웹 서버 접속하여 테스트**    
   브라우저에 http::/localhost:8080 (외부로 열었으면 http::/123.45.67.890:8080) 을 입력하여 접속합니다.

---

## 🎛️ 실행 CLI 옵션 정리

| 옵션                        | 값 예시                      | 설명                                                                                                                            |
| ------------------------- |---------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `--mysql_ip`              | `123.45.67.890`           | **필수**. 연결할 MySQL 서버 IP                                                                                                       |
| `--host`                  | `local \| <IP> \| docker` | Flask 바인딩 주소 <br>·`local에서만 구동` → `local` <br>·`본인 ip 사용` → `<IP>` (예시: `123.45.67.890`)  <br>· 만약 docker에서 실행할 경우 → `docker` |
| `--manage`                | *(플래그)*                   | CSV → DB 시드 & 테이블 초기화 후 종료                                                                                                    |
| `--internal_docker_mysql` | *(플래그)*                   | 서버 Docker와 mysql Docker를 같은 pc에서 구동할 때 사용<br> =>컨테이너 내부에서 `host.docker.internal` 사용                                           |


---

## 🔧 프로젝트 디렉토리 구조 

```text
laptopPT/
├── app.py                       # 실행 엔트리포인트, CLI로 여러 동작 실행
├── requirements.txt             # Python 패키지 목록
├── README.md                    # 이 파일
├── laptopDB.py                  # SQLAlchemy로 DB 모델 정의
├── routes/                      # 웹 라우팅 분리 모듈
│   ├── __init__.py
│   └── web.py                   # configure_routes(app): 전체 라우팅
│   ├── home.py
│   ├── basic_search.py
│   ├── advanced_search.py
│   ├── results.py
│   └── detail.py
│
├── seed/                        # DB 초기화·업데이트용
│   ├── seed_db.py               # CSV → MySQL 적재 스크립트
│   └── *.csv                    # 초기 데이터 파일들
│
├── laptopDB/                    # SQLAlchemy 모델
│   ├── __init__.py
│   ├── notebook.py
│   ├── cpu.py
│   ├── gpu.py
│   ├── display.py
│   └── convenience_feature.py
│
├── templates/                   # Jinja2 템플릿
│   ├── base.html
│   ├── home.html
│   ├── basic_search.html
│   ├── advanced_search.html
│   ├── results.html
│   └── notebook_detail.html
│
├── static/                    # css파일인데, Tailwind CSS 써서 사용 안한 상태. 필요시 사용
│   └── style.css
│
└── docker/                      # Docker 스택
    ├── mysql_server_docker/
    │   ├── docker-compose.yml
    │   ├── conf.d/my.cnf
    │   └── initdb/init.sql
    │
    └── laptopPT_server_docker/
        ├── Dockerfile
        ├── docker-compose.yml
        ├── entrypoint.sh
        └── .env
```

---

## 🐳 Docker 실행 (선택)

프로젝트에는 **두 개의 Docker 스택**이 포함돼 있습니다.

| 폴더                               | 설명                                                                                                    |
| -------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `docker/mysql_server_docker/`    | 독립형 MySQL 8 스택. 한 줄로 DB 서버를 띄우고 외부 `3306` 노출. 자세한 사용법은 폴더 내부 **README** 참고.                           |
| `docker/laptopPT_server_docker/` | Flask 서버 스택. `.env` 한 장으로 IP·호스트·초기화 여부를 설정. Docker Compose 한 줄로 빌드·실행. 자세한 사용법은 폴더 내부 **README** 참고. |

> **요약 실행 순서**
>
> 1. **DB**: `docker/mysql_server_docker` → `docker compose up -d`
> 2. **Flask**: `.env` 본인에 맞게 수정 후 `docker/laptopPT_server_docker` → `docker compose up --build -d`
