import requests
from apscheduler.schedulers.background import BackgroundScheduler
from .config import load_config
from zoneinfo import ZoneInfo

# スケジューラに日本時間(Asia/Tokyo)を設定
scheduler = BackgroundScheduler(timezone=ZoneInfo('Asia/Tokyo'))

# 風況取得関数
def fetch_wind():
    cfg = load_config()
    url = 'https://api.tomorrow.io/v4/timelines'
    params = {
        'apikey': cfg['tomorrow_api_key'],
        'location': f"{cfg['lat']},{cfg['lon']}",
        'fields': ['windSpeed','windDirection'],
        'units': 'metric',
        'timesteps': '1h',
        'startTime': 'now',
        'endTime': 'nowPlus1h',
        'altitude': int(cfg['alt'])
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()['data']['timelines'][0]['intervals'][0]['values']
    return data['windSpeed'], data['windDirection']

# 通知ジョブ（Pushover送信）
def notify_job():
    ws, wd = fetch_wind()
    cfg = load_config()
    po_url = 'https://api.pushover.net/1/messages.json'
    msg = f"【高度{cfg['alt']}m】風速: {ws:.1f} m/s, 風向: {wd:.0f}°"
    payload = {
        'token': cfg['pushover_app_token'],
        'user': cfg['pushover_user_key'],
        'message': msg
    }
    res = requests.post(po_url, data=payload)
    res.raise_for_status()

# スケジュール登録
def schedule_jobs():
    cfg = load_config()
    scheduler.remove_all_jobs()
    days = ','.join(cfg.get('days', [])) or '*'
    hour, minute = map(int, cfg.get('time', '00:00').split(':'))
    scheduler.add_job(
        notify_job,
        'cron',
        day_of_week=days,
        hour=hour,
        minute=minute,
        id='drone_job'
    )
    if not scheduler.running:
        scheduler.start()
