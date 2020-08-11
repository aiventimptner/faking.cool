#!/bin/bash

set -e

ssh-keyscan -H "$HOST" >>~/.ssh/known_hosts

ssh -p "$PORT" "$USERNAME@$HOST" << EOF
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