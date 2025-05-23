import os
import json
from flask import render_template, request, redirect, url_for, flash
from .jobs import fetch_wind, notify_job, schedule_jobs
from .config import load_config


def register_routes(app):

    @app.route('/')
    def dashboard():
        cfg = load_config()
        try:
            ws, wd = fetch_wind()
        except Exception as e:
            ws, wd = None, None
            flash(f'風況取得エラー: {e}')
        return render_template('dashboard.html', wind_speed=ws, wind_dir=wd, config=cfg)

    @app.route('/settings', methods=['GET', 'POST'])
    def settings():
        if request.method == 'POST':
            cfg = {
                'tomorrow_api_key': request.form['tomorrow_api_key'],
                'pushover_app_token': request.form['pushover_app_token'],
                'pushover_user_key': request.form['pushover_user_key'],
                'lat': float(request.form['lat']),
                'lon': float(request.form['lon']),
                'alt': int(request.form['alt']),
                'days': request.form.getlist('days'),
                'time': request.form['time']
            }
            with open('config.json', 'w') as f:
                json.dump(cfg, f, indent=2)
            schedule_jobs()
            flash('設定を保存しました')
            return redirect(url_for('settings'))
        cfg = load_config()
        return render_template('settings.html', config=cfg)

    @app.route('/test', methods=['POST'])
    def test_execution():
        try:
            notify_job()
            flash('テスト通知を送信しました')
        except Exception as e:
            flash(f'テスト実行エラー: {e}')
        return redirect(url_for('settings'))
