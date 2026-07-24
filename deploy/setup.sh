#!/bin/bash
# EDUQASH PRO V2.0 VPS Automated Setup Script (Ubuntu Server)
set -e

echo "=== 1. Tizim paketlarini yangilash hamda Nginx, Redis, PostgreSQL o'rnatish ==="
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv python3-dev build-essential libpq-dev nginx redis-server postgresql postgresql-contrib certbot python3-certbot-nginx git curl

echo "=== 2. Redis va PostgreSQL xizmatlarini yoqish ==="
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl enable postgresql
sudo systemctl start postgresql

echo "=== 3. Loyiha virtualenv muhitini yaratish va bog'liqliklarni o'rnatish ==="
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "=== 4. Statika yig'ish va Database Migration bajarish ==="
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "=== 5. Systemd servislarni sozlash va ulash ==="
sudo cp deploy/eduqash.service /etc/systemd/system/
sudo cp deploy/eduqash-celery.service /etc/systemd/system/
sudo cp deploy/eduqash-bot.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable eduqash eduqash-celery eduqash-bot
sudo systemctl restart eduqash eduqash-celery eduqash-bot

echo "=== 6. Nginx konfiguratsiyasini ulash ==="
sudo cp deploy/nginx.conf /etc/nginx/sites-available/eduqash
sudo ln -sf /etc/nginx/sites-available/eduqash /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "=== ✅ Sozlash to'liq muvaffaqiyatli yakunlandi! ==="
