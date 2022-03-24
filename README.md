# orchestrator
Service Chain Orchestrator using Python Flask and Apache Server

Clone this source code as below
```
git clone git@github.com:kukkalli/orchestrator.git
```

[Initial Setup](readme/initial-setup.md#initial-setup)

[Create Virtual Environment](readme/venv.md#virtual-environment-without-service)

[Start the app using Gunicorn](readme/gunicorn.md#gunicorn-setup)

[Service setup with apache reverse proxy](readme/flask_service.md#service-setup)

Set user ```<username>``` to use docker without root/sudo

```
sudo usermod -aG docker ```<username>```

sudo systemctl daemon-reload

sudo systemctl restart docker
```


Install ```docker-compose```

```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

docker-compose installation from [digitalocean.com](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04) webpage

```
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
sudo chown $USER /var/run/docker.sock
docker compose version
```

Place the ```create-docker.sh``` file on same level as the orchestrator directory.

```
hanif@kukkalli:~/PycharmProjects$ ll
total 24
drwxrwxr-x  5 hanif hanif 4096 Mär 10 14:53 ./
drwxr-xr-x 20 hanif hanif 4096 Mär 15 15:39 ../
-rwxrwxr-x  1 hanif hanif  371 Mär  1 19:49 create-docker.sh*
drwxrwxr-x 18 hanif hanif 4096 Mär 22 12:19 orchestrator/
```

