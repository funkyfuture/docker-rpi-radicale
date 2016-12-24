FROM armhf/python:3.5-alpine

LABEL org.label-schema.description="A Radicale image for the Raspberry Pi." \
      org.label-schema.name="rpi-radicale" \
      org.label-schema.version="1.1.1" \
      org.label-schema.usage="/README.md" \
      org.label-schema.url="https://hub.docker.com/r/funkyfuture/rpi-radicale" \
      org.label-schema.vcs-url="https://github.com/funkyfuture/docker-rpi-radicale"

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["/entrypoint.py"]
EXPOSE 5232
VOLUME /collections /config

ADD entrypoint.py README.md /

ENV RADICALE_VERSION=1.1.1
RUN apk add --no-cache apr apr-util libffi su-exec tini \
 && apk add --no-cache --virtual .build-deps apache2-utils ca-certificates build-base libffi-dev \
 && pip install --no-cache-dir bcrypt dulwich passlib radicale==$RADICALE_VERSION \
 && cp /usr/bin/htdigest /usr/bin/htpasswd /tmp \
 && adduser -s /bin/false -D -H radicale \
 && apk del .build-deps \
 && mv /tmp/htdigest /tmp/htpasswd /usr/bin
