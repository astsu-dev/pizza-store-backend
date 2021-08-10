# Pizza Store Backend

## Installation

### With poetry

Without development dependencies:

```shell
$ poetry install --no-dev
```

With development dependencies:

```shell
$ poetry install
```

### With pip

Without development dependencies:

```shell
$ pip install -r requirements.txt
```

With development dependencies:

```shell
$ pip install -r requirements-dev.txt
```


## Enviroment variables

You should create .env file for pass environment variables.

List of variables:

- SERVER_HOST - application server host. Has not default value;
- SERVER_PORT - application server port. Has not default value;
- JWT_SERCRET - application jwt secret key. Has not default value;
- JWT_ALOGRITHM - application jwt algorithm. Default value is "HS256";
- JWT_EXPIRES_IN - application jwt access token lifetime. Has no default value;
- JWT_REFRESH_TOKEN_EXPIRES_IN - application jwt refresh lifetime. Has no default value;
- POSTGRES_USER - database username. Has no default value;
- POSTGRES_PASSWORD - database password. Has no default value;
- POSTGRES_DB - database name. Has no default value;
- POSTGRES_HOST - database host for application. Has no default value;
- POSTGRES_PORT - database port. Has no default value;
- NGINX_PORT - port which nginx will be listen. Has no default value.

## Docker

You can run database, app and nginx by execute the following command:

```shell
$ docker-compose up
```
