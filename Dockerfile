FROM python:3.6-alpine

WORKDIR /usr/src/app

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add bash && apk add libffi-dev &&\
    apk add tree

ENV DJANGO_SETTINGS_MODULE=settings.settings

COPY requirements.txt ./
RUN /bin/bash -c "pip install --no-cache-dir -r requirements.txt"

RUN mkdir logs
COPY backend ./backend
WORKDIR /usr/src/app/backend
RUN /bin/bash -c "python manage.py migrate"
RUN /bin/bash -c "python manage.py loaddata users.json"
EXPOSE 8000

ENTRYPOINT [ "/usr/local/bin/gunicorn", "settings.wsgi", "-b 0:8000" ]