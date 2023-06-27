### Getting started

1) install venv
2) clone project
3) enter project base directory `alif-tech-test`
4) change `.env.dist` to `.env` and change environment variables to yours
5) python `python -m venv` and activate it
6) install `python install -r requirements.txt` file
7) run `alembic upgrade head`
8) auto populate command creates fake data `python main.py auto_populate`
9) using notification command `python main.py reserve_room`

### Generating Secret Key

```shell
openssl rand -hex 32
```

### Migration commands

Migration commands can be found in `alembic` directory

### .env file

```
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_HOST=
DB_PORT=
DEBUG=
```

### SMTP

```
SMTP_SERVER=
SENDER_EMAIL=
SENDER_PASSWORD=
```

### Twilio

```
ACCOUNT_SID=
AUTH_TOKEN=
TWILIO_NUMBER=
```

