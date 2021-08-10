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

Variables:

| Variable                     | Description                                        | Required | Default value |
|------------------------------|----------------------------------------------------|----------|---------------|
| SERVER_HOST                  | Application server host.                           | Yes      |               |
| SERVER_PORT                  | Application server port.                           | Yes      |               |
| JWT_SECRET                   | Application jwt secret key.                        | Yes      |               |
| JWT_ALGORITHM                | Application jwt algorithm.                         | No       | HS256         |
| JWT_EXPIRES_IN               | Application jwt access token lifetime in seconds.  | Yes      |               |
| JWT_REFRESH_TOKEN_EXPIRES_IN | Application jwt refresh token lifetime in seconds. | Yes      |               |
| POSTGRES_USER                | Database username.                                 | Yes      |               |
| POSTGRES_PASSWORD            | Database password.                                 | Yes      |               |
| POSTGRES_DB                  | Database name.                                     | Yes      |               |
| POSTGRES_HOST                | Database host for application.                     | Yes      |               |
| POSTGRES_PORT                | Database port.                                     | Yes      |               |
| NGINX_PORT                   | Port which nginx will be listen.                   | Yes      |               |

## Docker

You can run database, app and nginx by execute the following command:

```shell
$ docker-compose up
```
