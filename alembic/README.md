## Using Asyncio with Alembic

```shell
alembic init alembic -t directory
```

## Alembic auto generate migrations

```shell
alembic revision --autogenerate -m "Added account table"
```

## Alembic migrate

```shell
alembic upgrade head
```