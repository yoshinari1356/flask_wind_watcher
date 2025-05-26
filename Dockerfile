FROM python:3.10-slim

# 作業ディレクトリ
WORKDIR /app
ENV PYTHONPATH=/app
# cron は不要なら省略可能
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# 依存ライブラリ
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリコピー
COPY . /app

# appフォルダの __init__.py を保証
RUN mkdir -p /app/app && test -f /app/app/__init__.py || touch /app/app/__init__.py

EXPOSE 5000
CMD ["python3", "run.py"]
