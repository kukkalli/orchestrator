# Gunicorn Setup

### Install Gunicorn
```
pip install gunicorn
```

### Start virtual environment
```
source venv/bin/activate
```

### Start the application
```
gunicorn --bind 127.0.0.1:8080 wsgi:app
```
#### Sample Execution
```
(venv) hanif@kukkalli:~/PycharmProjects/orchestrator$ gunicorn --bind 127.0.0.1:8080 wsgi:app
[2022-02-03 16:04:15 +0100] [27134] [INFO] Starting gunicorn 20.1.0
[2022-02-03 16:04:15 +0100] [27134] [INFO] Listening at: http://127.0.0.1:8080 (27134)
[2022-02-03 16:04:15 +0100] [27134] [INFO] Using worker: sync
[2022-02-03 16:04:15 +0100] [27135] [INFO] Booting worker with pid: 27135
```

### Deactivate venv
```
deactivate
```

