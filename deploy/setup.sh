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
PROJECT_DIR=$(pwd)
CURRENT_USER=$(whoami)
CURRENT_GROUP=$(id -gn)

sed -e "s|/home/ubuntu/eduqash2|$PROJECT_DIR|g" -e "s|User=ubuntu|User=$CURRENT_USER|g" -e "s|Group=www-data|Group=$CURRENT_GROUP|g" deploy/eduqash.service | sudo tee /etc/systemd/system/eduqash.service > /dev/null
sed -e "s|/home/ubuntu/eduqash2|$PROJECT_DIR|g" -e "s|User=ubuntu|User=$CURRENT_USER|g" -e "s|Group=www-data|Group=$CURRENT_GROUP|g" deploy/eduqash-celery.service | sudo tee /etc/systemd/system/eduqash-celery.service > /dev/null
sed -e "s|/home/ubuntu/eduqash2|$PROJECT_DIR|g" -e "s|User=ubuntu|User=$CURRENT_USER|g" -e "s|Group=www-data|Group=$CURRENT_GROUP|g" deploy/eduqash-bot.service | sudo tee /etc/systemd/system/eduqash-bot.service > /dev/null

sudo systemctl daemon-reload
sudo systemctl enable eduqash eduqash-celery eduqash-bot
sudo systemctl restart eduqash eduqash-celery eduqash-bot

echo "=== 6. Nginx konfiguratsiyasini ulash ==="
sed -e "s|/home/ubuntu/eduqash2|$PROJECT_DIR|g" deploy/nginx.conf | sudo tee /etc/nginx/sites-available/eduqash > /dev/null
sudo ln -sf /etc/nginx/sites-available/eduqash /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "=== ✅ Sozlash to'liq muvaffaqiyatli yakunlandi! ==="
