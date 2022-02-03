# Virtual Environment without Service

### Set virtual environment
```
python3 -m venv venv
```

### Start virtual environment
```
source venv/bin/activate
```

### Start the application
```
python ~/orchestrator/app.py
```

### Example
```
hanif@kukkalli:~/PycharmProjects/orchestrator$ source venv/bin/activate
(venv) hanif@kukkalli:~/PycharmProjects/orchestrator$ python app.py 
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 134-907-213
```

### Test the service
```
curl -i -H "Content-Type: application/json" -X POST -d '{"number":28}' http://127.0.0.1:8080/getSquare

hanif@kukkalli:~/PycharmProjects/orchestrator$ curl -i -H "Content-Type: application/json" -X POST -d '{"number":28}' http://127.0.0.1:8080/getSquare
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 20
Server: Werkzeug/2.0.2 Python/3.9.5
Date: Thu, 03 Feb 2022 14:57:05 GMT

{
  "answer": 784
}



curl -i -H "Content-Type: application/json" -X GET http://127.0.0.1:8080/

hanif@kukkalli:~/PycharmProjects/orchestrator$ curl -i -H "Content-Type: application/json" -X GET http://127.0.0.1:8080/
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 55
Server: Werkzeug/2.0.2 Python/3.9.5
Date: Thu, 03 Feb 2022 14:58:04 GMT

{
  "dob": "1984-11-01", 
  "name": "Hanif Kukkalli"
}

```

### Deactivate venv
```
deactivate
```
