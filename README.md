# Drone Notify Flask App

## サービス概要

このアプリケーションは、指定した地点・高度の風速および風向をリアルタイムで取得し、
定期的にPushover通知を送信するドローン飛行支援ツールです。Webダッシュボードから設定変更、
テスト実行、現在の風況確認が可能です。

主な機能:

* 指定地点（緯度・経度）と高度での風速・風向取得（Tomorrow\.io API）
* 日本時間(Asia/Tokyo)での曜日・時刻指定による定期通知
* Pushoverによるプッシュ通知
* Web UIでAPIキー／通知先設定、通知スケジュールの管理
* ダッシュボードで現在の風況と設定内容を確認
* テスト通知機能

## プロジェクト構成

```
├── Dockerfile
├── requirements.txt
├── run.py                # アプリ起動エントリ
├── config.json           # 設定ファイル（初回起動時に生成）
├── app/                  # アプリケーションモジュール
│   ├── __init__.py       # アプリファクトリ
│   ├── config.py         # 設定読み込み
│   ├── jobs.py           # ジョブ定義／データ取得／スケジュール
│   └── routes.py         # ルーティング定義
└── templates/
    ├── dashboard.html    # ダッシュボード画面
    └── settings.html     # 設定画面
```

## セットアップ方法

1. リポジトリをクローン

   ```bash
   git clone git@github.com:yoshinari1356/flask_wind_watcher.git
   cd python_wind_watcher
   ```

2. 実行方法

   ```bash
   docker compose up
   ```


## 利用サービスと必要なトークン

* Tomorrow.io API
  * 風況（風速・風向）取得用

* Pushover
  * プッシュ通知用

## TODOリスト

- [ ] UIをreactに変更
  - [x] settings
  - [ ] dashboard
- [ ] 地図表示との連携による地点選択UIの実装
- [ ] 風向のビジュアル化（矢印アイコン／コンパスローズ表示）
- [ ] 過去・予報データのグラフ化および履歴管理（SQLite/PostgreSQL対応）
- [ ] 通知チャネルの拡張（Slack, Telegram, Email, Webhook など）
- [ ] ユーザー認証・マルチユーザー対応機能の追加
- [ ] 運行ログと履歴エクスポート（CSV/DB, ロギング基盤連携）
- [ ] テスト・CI/CDパイプライン構築（自動テスト・ビルド・デプロイ）
- [ ] Docker/Kubernetes 運用強化（Helm, ロギング, モニタリング）
- [ ] 多言語化・ローカライズ対応
- [ ] モバイル対応／PWA化
- [ ] アクセシビリティ改善（ダークモード, スクリーンリーダー対応など）
- [ ] APIキャッシュおよびレート制限管理

---

© 2025 Drone Notify Project
