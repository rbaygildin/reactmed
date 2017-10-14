# Reactmed
## Links
### Deployement
  1. https://www.digitalocean.com/community/tutorials/nginx-ubuntu-16-04-ru 
  2. https://khashtamov.com/ru/how-to-deploy-django-app/
### Machine Learning in diagnosis
  1. [Datasets](https://vincentarelbundock.github.io/Rdatasets/datasets.html)
  2. [Machine learning open course](https://habrahabr.ru/company/ods/blog/326418/)
## Deploying
First of all it's important to clone project into local directory
```bash
git clone https://github.com/reactmed/reactmed.git 
```
You can use SSH instead HTTPS
```bash
git clone git@github.com:reactmed/reactmed.git
```
Then you have to install python 3 and pip
```bash
sudo apt-get update 
sudo apt-get install python3
sudo apt-get install python3-pip
```

After installing python 3 and pip you should install virtualenv
```bash
sudo pip3 install virtualenv
```
Prepare virtual environment
```bash
mkdir venv
virtualenv -p python3 --no-site-packages venv
```

As soon as you install executable environment you activate virtual environment
```bash
source venv/bin/activate
```

To install python packages run command
``` bash
pip install --no-cache-dir -r requirements.txt
```

To prepare database run following command
```bash
./manage.py migrate
```

To start application run command
```bash
./manage.py runserver 0.0.0.0:8080
```
Or 
```bash
nohup ./manage.py runserver 0.0.0.0:8080 &
```

That's All! You're all set! My congratulations


