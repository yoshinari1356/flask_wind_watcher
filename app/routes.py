import os
import json
from flask import render_template, request, redirect, url_for, flash, jsonify
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

    # API
    @app.route('/api/routes', methods=['GET'])
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'url': str(rule)
            })
        return jsonify(routes)

    @app.route('/api/settings', methods=['GET', 'POST'])
    def api_settings():
        print(f"api_settings called with method: {request.method}")
        if request.method == 'POST':
            print("Processing POST request")
            try:
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
                print(f"Received config: {cfg}")

                with open('config.json', 'w') as f:
                    json.dump(cfg, f, indent=2)
                print("Config saved to file")

                schedule_jobs()
                print("Jobs rescheduled")

                return jsonify({"message": "Settings updated successfully"})
            except Exception as e:
                print(f"Error in POST processing: {str(e)}")
                return jsonify({"error": str(e)}), 500
        else:
            print("Processing GET request")
            try:
                cfg = load_config()
                print(f"Loaded config: {cfg}")
                return jsonify(cfg)
            except Exception as e:
                print(f"Error loading config: {str(e)}")
                return jsonify({"error": str(e)}), 500

    @app.route('/api/wind', methods=['GET'])
    def api_wind():
        try:
            ws, wd = fetch_wind()
            return jsonify({'wind_speed': ws, 'wind_dir': wd})
        except Exception as e:
            return jsonify({'error': str(e)}), 500