import sys
from flask import Flask
from laptopDB import db
from routes.web import configure_routes
from seed.seed_db import initialize_db


def parse_args():
    args = sys.argv
    options = {
        "use_internal_mysql": "--internal_docker_mysql" in args,
        "is_manage": "--manage" in args,
        "mysql_ip": None,
        "host": "127.0.0.1",  # 기본값은 local
    }

    for i, arg in enumerate(args):
        if arg == "--mysql_ip" and i + 1 < len(args):
            options["mysql_ip"] = args[i + 1]
        elif arg == "--host" and i + 1 < len(args):
            val = args[i + 1]
            if val == "docker":
                options["host"] = "0.0.0.0"
            elif val == "local":
                options["host"] = "127.0.0.1"
            else:
                options["host"] = val

    return options


def get_db_uri(use_internal: bool, mysql_ip: str) -> str:
    if use_internal:
        host = "host.docker.internal"
    elif mysql_ip:
        host = mysql_ip
    else:
        print("❌ Error: --mysql_ip [IP주소] 를 반드시 지정해야 합니다.")
        sys.exit(1)
    return f"mysql+pymysql://laptop_project_user:qwe123@{host}:3306/laptopPT"


def create_app(config) -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = get_db_uri(
        config["use_internal_mysql"], config["mysql_ip"]
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["SQLALCHEMY_ECHO"] = True
    db.init_app(app)
    return app


def run_web(app, host):
    with app.app_context():

        configure_routes(app)
        print(f"🚀 웹 서비스 실행 중... ({host}:8080)")
    app.run(debug=False, port=8080, host=host)


def run_manage(app):
    with app.app_context():
        print("🛠 DB 초기화 중...")
        db.drop_all()
        db.create_all()
        initialize_db()
        print("✅ DB 초기화 완료")


if __name__ == '__main__':
    config = parse_args()
    app = create_app(config)

    if config["is_manage"]:
        run_manage(app)
    else:
        run_web(app, config["host"])