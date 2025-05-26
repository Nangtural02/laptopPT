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

## 🚀 설치 및 실행
1. 소스코드 다운
  ```bash
  git clone https://github.com/Nangtural02/laptopPT.git
  cd laptopPT
  ```
2. **환경 준비**

   ```bash
   pip install -r requirements.txt
   ```
   그리고 app.py의 create_app에 SQL 서버 주소를 입력해줍니다. 💥💥💥💥💥💥💥💥💥💥💥💥💥부분만 수정하면됩니다. 💥대신에 서버주소를 넣어주세요.
   ```python
   # /* laptopPT/app.py */
   def create_app():
    app = Flask(__name__)

    # MySQL 연결 설정
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://laptop_project_user:qwe123@💥💥💥💥💥💥💥💥💥💥💥💥💥:3306/laptopPT'  # WSL MySQL 연결 URI   💥에 서버주소를 넣으세요
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 불필요한 메모리 사용 방지
    # app.config['SQLALCHEMY_ECHO'] = True #SQL 날아가는거 디버깅
    db.init_app(app)

    return app
   ```

3. **DB 초기화 & csv 데이터 삽입** (데이터 업데이트할때말곤 건드리지마세요!! 서버는 항상켜져있습니다)
   /seed/의 csv파일들로 DB서버의 각 테이블을 초기화/업데이트할 수 있습니다.
   csv파일을 수정한뒤, 터미널에서 아래와 같이 실행하면 DB서버가 업데이트 됩니다.
   ```bash
   python app.py --manage
   ```

4. **웹 서버 구동**

   ```bash
   python app.py (기본설정은 http::/localhost:8080입니다)
   ```
5. **웹 서버 접속하여 테스트**
   브라우저에 http::/localhost:8080 을 입력하여 접속합니다.
---

## 🔧 프로젝트 구조

```
project/
│
├── app.py      # 실행 엔트리포인트: 웹/관리 모드 전환
├── laptopDB.py            # SQLAlchemy 모델 정의
│
├── seed/                      # DB 관리용
│   ├── seed_db.py             # CSV → DB 적재용 모듈
│   └── *.csv                  # 초기 데이터 파일들
│
├── routes/                    # 웹 라우팅 분리 모듈
│   ├── home.py
│   ├── basic_search.py
│   ├── advanced_search.py
│   ├── results.py
│   ├── detail.py
│   └── web.py     # configure_routes(app): 전체 등록
│
├── templates/                 # Jinja2 템플릿

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
├── requirements.txt
└── README.md
```

---


