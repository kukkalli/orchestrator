# Service Setup

## Create ```systemd``` Unit File

### Create a file in the below path
```
sudo nano /etc/systemd/system/flaskrest.service
```

### Add in the contents in the file flaskrest.service
```
[Unit]
Description=Gunicorn instance to serve flask application
After=network.target

[Service]
User=hanif
Group=www-data
WorkingDirectory=/home/hanif/PycharmProjects/orchestrator/ 
Environment="PATH=/home/hanif/PycharmProjects/orchestrator/venv/bin"
ExecStart=/home/hanif/PycharmProjects/orchestrator/venv/bin/gunicorn --config gunicorn_config.py wsgi:app

[Install]
WantedBy=multi-user.target
```

Modify ```/home/hanif/PycharmProjects/``` with your path to orchestrator directory.

### Start and Enable flaskrest.service
```
sudo systemctl start flaskrest.service

sudo systemctl enable flaskrest.service
```

### Check the status of the created service
```
hanif@kukkalli:~/PycharmProjects/orchestrator$ service flaskrest status
● flaskrest.service - Gunicorn instance to serve flask application
     Loaded: loaded (/etc/systemd/system/flaskrest.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2022-02-03 16:09:27 CET; 52s ago
   Main PID: 27307 (gunicorn)
      Tasks: 19 (limit: 13072)
     Memory: 145.6M
     CGroup: /system.slice/flaskrest.service
             ├─27307 /home/hanif/PycharmProjects/orchestrator/venv/bin/python /home/hanif/PycharmProjects/orchestrator/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
             ├─27308 /home/hanif/PycharmProjects/orchestrator/venv/bin/python /home/hanif/PycharmProjects/orchestrator/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
             ├─27309 /home/hanif/PycharmProjects/orchestrator/venv/bin/python /home/hanif/PycharmProjects/orchestrator/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
             ├─27311 /home/hanif/PycharmProjects/orchestrator/venv/bin/python /home/hanif/PycharmProjects/orchestrator/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
             ├─27313 /home/hanif/PycharmProjects/orchestrator/venv/bin/python /home/hanif/PycharmProjects/orchestrator/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
             ├─27314 /home/hanif/PycharmProjects/orchestrator/venv/bin/python /home/hanif/PycharmProjects/orchestrator/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
             ├─27317 /home/hanif/PycharmProjects/orchestrator/venv/bin/python /home/hanif/PycharmProjects/orchestrator/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
             ├─27319 /home/hanif/PycharmProjects/orchestrator/venv/bin/python /home/hanif/PycharmProjects/orchestrator/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
             ├─27321 /home/hanif/PycharmProjects/orchestrator/venv/bin/python /home/hanif/PycharmProjects/orchestrator/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
             └─27323 /home/hanif/PycharmProjects/orchestrator/venv/bin/python /home/hanif/PycharmProjects/orchestrator/venv/bin/gunicorn --config gunicorn_config.py wsgi:app

Feb 03 16:09:27 kukkalli gunicorn[27307]: [2022-02-03 16:09:27 +0100] [27307] [INFO] Using worker: sync
Feb 03 16:09:27 kukkalli gunicorn[27308]: [2022-02-03 16:09:27 +0100] [27308] [INFO] Booting worker with pid: 27308
Feb 03 16:09:27 kukkalli gunicorn[27309]: [2022-02-03 16:09:27 +0100] [27309] [INFO] Booting worker with pid: 27309
Feb 03 16:09:27 kukkalli gunicorn[27311]: [2022-02-03 16:09:27 +0100] [27311] [INFO] Booting worker with pid: 27311
Feb 03 16:09:27 kukkalli gunicorn[27313]: [2022-02-03 16:09:27 +0100] [27313] [INFO] Booting worker with pid: 27313
Feb 03 16:09:27 kukkalli gunicorn[27314]: [2022-02-03 16:09:27 +0100] [27314] [INFO] Booting worker with pid: 27314
Feb 03 16:09:27 kukkalli gunicorn[27317]: [2022-02-03 16:09:27 +0100] [27317] [INFO] Booting worker with pid: 27317
Feb 03 16:09:28 kukkalli gunicorn[27319]: [2022-02-03 16:09:28 +0100] [27319] [INFO] Booting worker with pid: 27319
Feb 03 16:09:28 kukkalli gunicorn[27321]: [2022-02-03 16:09:28 +0100] [27321] [INFO] Booting worker with pid: 27321
Feb 03 16:09:28 kukkalli gunicorn[27323]: [2022-02-03 16:09:28 +0100] [27323] [INFO] Booting worker with pid: 27323
```

## Configuring Apache2 as a Reverse Proxy
### Install ```apache2``` server
```
sudo apt install apache2
```
### Enable proxy_http to enable ProxyPass
```
sudo a2enmod proxy_http
```

### Create apache2 configuration
```
sudo nano /etc/apache2/sites-available/flaskrest.conf
```

### Add the configuration as below:
```
<VirtualHost *:80>
        ServerAdmin hanif@kukkalli

        ErrorLog ${APACHE_LOG_DIR}/flaskrest-error.log
        CustomLog ${APACHE_LOG_DIR}/flaskrest-access.log combined

        <Location />
                ProxyPass unix:/home/hanif/PycharmProjects/orchestrator/flaskrest.sock|http://127.0.0.1/
                ProxyPassReverse unix:/home/hanif/PycharmProjects/orchestrator/flaskrest.sock|http://127.0.0.1/
        </Location>
</VirtualHost>
```

### Configure file to apache2

Create the symbolic link for the configuration file in the Apache2 sites-enabled directory manually
```
sudo ln -s /etc/apache2/sites-available/flaskrest.conf /etc/apache2/sites-enabled/
```


### Delete or Rename ```000-default.conf``` file in the ```/etc/apache2/sites-available/``` directory
```
mv 000-default.conf 000-default.conf.bkp
```


### Reload the Apache2 service
```
service apache2 restart
```


### Test the service
```
curl -i -H "Content-Type: application/json" -X POST -d '{"number":28}' http://127.0.0.1/getSquare

hanif@kukkalli:~$ curl -i -H "Content-Type: application/json" -X POST -d '{"number":28}' http://127.0.0.1/getSquare
HTTP/1.1 200 OK
Date: Thu, 03 Feb 2022 16:06:57 GMT
Server: gunicorn
Content-Type: application/json
Content-Length: 15

{"answer":784}



curl -i -H "Content-Type: application/json" -X GET http://127.0.0.1/

hanif@kukkalli:~$ curl -i -H "Content-Type: application/json" -X GET http://127.0.0.1/
HTTP/1.1 200 OK
Date: Thu, 03 Feb 2022 16:07:35 GMT
Server: gunicorn
Content-Type: application/json
Content-Length: 45

{"dob":"1984-11-01","name":"Hanif Kukkalli"}

```
