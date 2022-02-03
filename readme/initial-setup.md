# Initial Setup

## Environment
Linux Distribution: Ubuntu 20.04.1

### Install Python3
```
sudo apt install python3.8
```

### Set python3.9 as default
```
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
```

### Install pip
```
sudo apt install python3-pip
```

### Install git and subversion
```
sudo apt install git subversion
```

### Set virtual environment
```
python3 -m venv venv
```

### Upgrade pip
```
venv/bin/python -m pip install --upgrade pip
```

### Install flask
```
pip install flask
```

