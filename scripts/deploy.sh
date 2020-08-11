#!/usr/bin/env bash

sshpass -p "$PASSWORD" ssh "$USERNAME@$HOST" -p "$PORT" << EOF
cd $DIR
git pull
. venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --clear --no-input
python manage.py test
python manage.py check --deploy
deactivate
echo "$PASSWORD" | sudo -S systemctl restart gunicorn
systemctl status gunicorn
EOF