#!/bin/bash
set -e
# ssh-keyscan -H "$HOST" >> ~/.ssh/known_hosts

echo ">>>> Connect to remote location <<<<"
ssh -p "$PORT" "$USER@$HOST" << EOF
cd $DIR
echo ">>>> Update project files <<<<"
git pull
. venv/bin/activate
echo ">>>> Install packages <<<<"
pip install -r requirements.txt
echo ">>>> Check production environment <<<<"
python manage.py check --deploy
echo ">>>> Recollect statics <<<<"
python manage.py collectstatic --clear --no-input
echo ">>>> Migrate to database <<<<"
python manage.py migrate
deactivate
echo ">>>> Restart gunicorn service <<<<"
echo "$PASSWORD" | sudo -S systemctl restart gunicorn
systemctl status gunicorn
EOF