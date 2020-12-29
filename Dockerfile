FROM alpine:3

LABEL version="0.1.4"

RUN apk --update add \
    python3 \
    py3-pip \
    py3-aiohttp \
    lighttpd \
    && rm -rf /var/cache/apk/*

RUN pip3 install python-socketio

RUN adduser www-data -G www-data -H -s /bin/false -D && \
    mkdir -p /run/lighttpd/ && \
    chown www-data. /run/lighttpd/

# EXPOSE 8080/tcp

COPY backend/lighttpd.conf /etc/lighttpd/lighttpd.conf

COPY . /app

#CMD echo $PORT;\
#    if [ -z ${PORT+x} ]; then PORT=8080;fi;\
#    echo "Using port $PORT.";\
#    sed -i '$ d' /etc/lighttpd/lighttpd.conf;\
#    echo "server.port = $PORT" >> /etc/lighttpd/lighttpd.conf;\
#    cat /etc/lighttpd/lighttpd.conf;\
#    ./app/backend/server.py & lighttpd -D -f /etc/lighttpd/lighttpd.conf

CMD ./app/backend/server.py