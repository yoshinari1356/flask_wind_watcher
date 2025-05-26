import os
from flask import Flask
from .config import load_config
from .jobs import schedule_jobs
from flask_cors import CORS

def create_app():
    # テンプレートフォルダをルートのtemplatesに設定
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'change_this_secret')

    CORS(app)

    # スケジューラ起動
    schedule_jobs()

    # ルーティング登録
    from .routes import register_routes
    register_routes(app)

    return app

