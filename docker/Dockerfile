FROM ubuntu:20.04

LABEL maintainer="Hanif Kukkalli <hanif@kukkalli.com>"

RUN DEBIAN_FRONTEND=noninteractive apt update
RUN DEBIAN_FRONTEND=noninteractive apt -y dist-upgrade
RUN DEBIAN_FRONTEND=noninteractive apt -yq install net-tools nginx python3-pip
RUN DEBIAN_FRONTEND=noninteractive apt install openssl
RUN pip install --upgrade pip

# RUN openssl ecparam -name sect571r1 -genkey -noout -out kukkalli.com.pem
# RUN openssl req -new -sha256 -key kukkalli.com.pem -out kukkalli.com.csr
COPY docker/kukkalli.com.csr /etc/nginx/ssl/kukkalli.com.csr


# Install requirements
COPY app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN useradd -ms /bin/bash hanif
RUN useradd -ms /bin/bash nginx

# Expose basic http port
EXPOSE 80

# Expose 443, in case of LTS / HTTPS
EXPOSE 443

# Remove default configuration from Nginx
# RUN rm /etc/nginx/conf.d/default.conf

# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY docker/uwsgi.ini /etc/uwsgi/


# Install Supervisord
RUN apt update && apt install -y supervisor \
&& rm -rf /var/lib/apt/lists/*
# Custom Supervisord config
COPY docker/supervisord-debian.conf /etc/supervisor/conf.d/supervisord.conf

# Copy stop-supervisor.sh to kill the supervisor and substasks on app failure
COPY docker/stop-supervisor.sh /etc/supervisor/stop-supervisor.sh
RUN chmod +x /etc/supervisor/stop-supervisor.sh

# Which uWSGI .ini file should be used, to make it customizable
ENV UWSGI_INI /app/uwsgi.ini

# By default, run 2 processes
ENV UWSGI_CHEAPER 2

# By default, when on demand, run up to 16 processes
ENV UWSGI_PROCESSES 16

# By default, allow unlimited file sizes, modify it to limit the file sizes
# To have a maximum of 1 MB (Nginx's default) change the line to:
# ENV NGINX_MAX_UPLOAD 1m
ENV NGINX_MAX_UPLOAD 0

# By default, Nginx will run a single worker process, setting it to auto
# will create a worker for each CPU core
ENV NGINX_WORKER_PROCESSES 1

# By default, Nginx listens on port 80.
# To modify this, change LISTEN_PORT environment variable.
# (in a Dockerfile or with an option for `docker run`)
ENV LISTEN_PORT 80

# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /app/static

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
# ENV STATIC_INDEX 1
ENV STATIC_INDEX 0

# Copy start.sh script that will check for a /app/prestart.sh script and run it before starting the app
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

# Copy the entrypoint that will generate Nginx additional configs
# COPY orchestrator/docker/entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# ENTRYPOINT ["/entrypoint.sh"]

# Add demo app
COPY /app /app
WORKDIR /app

# Make /app/* available to be imported by Python globally to better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app


# Move the base entrypoint to reuse it
# COPY orchestrator/docker/uwsgi-nginx-entrypoint.sh /uwsgi-nginx-entrypoint.sh
# Copy the entrypoint that will generate Nginx additional configs
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Supervisor, which in turn will start Nginx and uWSGI
CMD ["/start.sh"]
