# вытянуть образ для сборки минимального образа
FROM python:3.10-alpine as Builder

# установить рабочую папку 
WORKDIR /app

# установить переменные среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# установить по для работы с postgresql и python3
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# установить по для игнора ошибок
# копирование файлов в образ
RUN pip install --upgrade pip
RUN pip install flake8==3.9.2
RUN flake8 --ignore=E501,F401 .

# установить бинарные зависимости для проекта
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


# основной образ для работы
FROM python:3.10-alpine

# установить рабочую папку для этого образа
WORKDIR /app
ENV APP_HOME=/app

# создать пользователя и группу app 
#RUN addgroup -S app && adduser -S app -G app

# скопировать из образа выше установленные зависимости для проекта
# установить в этот образ
RUN apk update && apk add libpq
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# скопировать проект в рабочую папку в образ
COPY . .
#RUN python manage.py collectstatic --noinput


# изменить владельца и группу для рабочего каталога
#RUN chown -R app:app $APP_HOME
#USER app