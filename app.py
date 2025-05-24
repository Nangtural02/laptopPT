import sys
from flask import Flask
from laptopDB import db

# 경로에 따라 나눌 예정
from routes.web import configure_routes
from seed.seed_db import initialize_db


def create_app():
    app = Flask(__name__)

    # MySQL 연결 설정
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://laptop_project_user:qwe123@💥💥💥💥💥💥💥💥💥💥💥💥/laptopPT'  # WSL MySQL 연결 URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 불필요한 메모리 사용 방지
    # app.config['SQLALCHEMY_ECHO'] = True #SQL 날아가는거 디버깅
    db.init_app(app)

    return app


def run_web(app):

    with app.app_context():
        configure_routes(app)  # 실제 라우트 설정
        print("🚀 웹 서비스 모드로 실행 중...")
    app.run(debug=True, port=8080, host="💥💥💥💥💥💥💥💥💥💥💥💥")


def run_manage(app):
    with app.app_context():
        print("🛠 DB 초기화 및 데이터 삽입 중...")
        db.drop_all()
        db.create_all()
        initialize_db()  # CSV 기반 초기화 예정
        print("✅ DB 초기화 완료")


if __name__ == '__main__':
    app = create_app()
    if '--manage' in sys.argv:
        run_manage(app)
    else:
        run_web(app)
