
# Generate SECRET_KEY
```
$ openssl rand -hex 32
```

# Copy & change .env file
```
$ cp .env.example .env
```

# Build app
```
$ docker-compose up --build --remove-orphans
```

# Access docker
```
$ docker exec -it app bash
```

# Migrate DB

```
$ alembic init migrations
$ alembic revision --autogenerate -m "{New revision}"
$ app alembic upgrade head
```

# Unit test
```
$ pytest
```