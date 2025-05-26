import os
from flask import Flask, current_app
from .config import load_config
from .jobs import schedule_jobs
from flask_cors import CORS
import logging

def create_app():
    # テンプレートフォルダをルートのtemplatesに設定
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'change_this_secret')

    with app.app_context():
        current_app.logger.info("App initialized")

    CORS(app)

    # スケジューラ起動
    schedule_jobs()

    # ルーティング登録
    from .routes import register_routes
    register_routes(app)

    # ログ設定
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 既存のハンドラーを確認し、重複を避ける
    if not logger.handlers:
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return app

