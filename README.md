
## Environment settings

Generate a new secure key
```python
from django.core.management import utils
utils.get_random_secret_key()
```

#### Example .env file
```.env
SECRET_KEY="secret"

ALLOWED_HOSTS="domain.tld,second-domain.tld"

DB_ENGINE=django.db.backends.postgresql
DB_NAME=
DB_HOST=
DB_PORT=
DB_USERNAME=
DB_PASSWORD=

SMTP_HOST=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
```