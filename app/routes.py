import os
import json
from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from .jobs import fetch_wind, notify_job, schedule_jobs
from .config import load_config

def register_routes(app):

    @app.route('/')
    def dashboard():
        current_app.logger.info('dashboard')
        cfg = load_config()
        try:
            ws, wd = fetch_wind()
        except Exception as e:
            ws, wd = None, None
            flash(f'風況取得エラー: {e}')
        return render_template('dashboard.html', wind_speed=ws, wind_dir=wd, config=cfg)

    @app.route('/settings', methods=['GET', 'POST'])
    def settings():
        current_app.logger.info('settings')
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
        current_app.logger.info('test_execution')
        try:
            notify_job()
            flash('テスト通知を送信しました')
        except Exception as e:
            flash(f'テスト実行エラー: {e}')
        return redirect(url_for('settings'))

    # API
    @app.route('/api/routes', methods=['GET'])
    def list_routes():
        current_app.logger.info('list_routes')
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
        current_app.logger.info(f"api_settings called with method: {request.method}")
        if request.method == 'POST':
            current_app.logger.info("Processing POST request")
            try:
                data = request.get_json()  # JSONデータを取得
                current_app.logger.info("1")
                if data is None:
                    current_app.logger.info("err 1")
                    return {"error": "Invalid JSON"}, 400  # JSONが無効な場合のエラーレスポンス

                current_app.logger.info(data)
                # if 'required_field' not in data:
                #     current_app.logger.info("err 2")
                #     return {"error": "Required field 'required_field' is missing"}, 400

                cfg = {
                    'tomorrow_api_key': data['tomorrow_api_key'],
                    'pushover_app_token': data['pushover_app_token'],
                    'pushover_user_key': data['pushover_user_key'],
                    'lat': float(data['lat']),
                    'lon': float(data['lon']),
                    'alt': int(data['alt']),
                    'days': data['days'],
                    'time': data['time']
                }

                with open('config.json', 'w') as f:
                    json.dump(cfg, f, indent=2)

                schedule_jobs()

                return jsonify({"message": "Settings updated successfully"})
            except Exception as e:
                current_app.logger.debug(f"Error in POST processing: {str(e)}")
                return jsonify({"error": str(e)}), 500
        else:
            current_app.logger.info("Processing GET request")
            try:
                cfg = load_config()
                return jsonify(cfg)
            except Exception as e:
                current_app.logger.debug(f"Error loading config: {str(e)}")
                return jsonify({"error": str(e)}), 500

    @app.route('/api/wind', methods=['GET'])
    def api_wind():
        current_app.logger.info('api_wind')
        try:
            ws, wd = fetch_wind()
            return jsonify({'wind_speed': ws, 'wind_dir': wd})
        except Exception as e:
            current_app.logger.debug(f"Error in api_wind: {str(e)}")
            return jsonify({'error': str(e)}), 500