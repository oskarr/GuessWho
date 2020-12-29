FROM alpine:3

LABEL version="0.1"

RUN apk --update add \
    python3 \
    py3-pip \
    py3-aiohttp \
    && rm -rf /var/cache/apk/*

RUN pip3 install python-socketio

# Uncomment these if not running on Heroku.
#ENV PORT=8080
#EXPOSE 8080/tcp

COPY . /app

CMD ./app/backend/server.py