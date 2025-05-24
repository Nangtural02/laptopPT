# 노트북 견적좀짜줘 너 컴공이잖아



## 서비스 흐름
[홈 화면]
    ↓
[기초 검색] or [상세 검색]
    ↓
POST → /results
    ↓
[검색 결과 리스트 출력]


## 프로젝트 구조
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
├── static/                    # 정적 자원 (선택 사항)
│   └── style.css
│
├── requirements.txt
└── README.md

