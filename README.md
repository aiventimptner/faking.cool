# Fakultät der Ingenieure

The faculty of engineers (german: "Fakultät der Ingenieure", abbr. "faking") is a cooperation between three student 
representatives at the [Otto-von-Guericke-University Magdeburg](https://www.ovgu.de). The three student representatives are:

- [Student council of the faculty for mechanical engineering](https://farafmb.de)
- [Student council of the faculty for electrical engineering and information technology](https://www.farafeit.de)
- [Student council of the faculty for process and systems engineering](https://www.farafvst.ovgu.de)

The website makes use of [Django](https://www.djangoproject.com) and [Bulma](https://bulma.io)

## Installation

Rename `.env.example` to `.env` and supply all credentials.

You can generate a new secure key for your `.env`.

```python
from django.core.management import utils
utils.get_random_secret_key()
```

To run a local development server:

```shell
python manage.py runserver
```

To run all tests:

```shell
python manage.py test
```

## License

[MIT](https://github.com/aiventimptner/faking/blob/main/LICENSE)
