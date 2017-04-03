FROM alpine
RUN apk --update-cache add ca-certificates python py-pip \
    && pip install -U pip \
    && rm -rf /var/cache/apk/*
ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app
EXPOSE 8080
ENTRYPOINT ["/usr/bin/gunicorn"]
CMD ["--access-logfile", "-", "--error-logfile", "-", "--bind", "0.0.0.0:8080", "daily_spent:app"]
