import os
import json

CONFIG_PATH = 'config.json'

def load_config(path=CONFIG_PATH):
    default = {
        "tomorrow_api_key": os.getenv('TOMORROW_API_KEY', ''),
        "pushover_app_token": os.getenv('PUSHOVER_APP_TOKEN', ''),
        "pushover_user_key": os.getenv('PUSHOVER_USER_KEY', ''),
        "lat": 35.6895,
        "lon": 139.6917,
        "alt": 100,
        "days": ["mon","thu"],
        "time": "07:30"
    }
    # ファイルがない場合、初期化して返す
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump(default, f, indent=2)
        return default
    # JSON 読み込み
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # 不正な場合は初期化
        with open(path, 'w') as f:
            json.dump(default, f, indent=2)
        return default
