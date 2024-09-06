# REST API - TASK MANAGEMENT SYSTEM 
This is the sample api for web app which helps manger to list out the task and assign to users.

## Getting started
To get started you can simply clone this sportsbasket project repository and install the dependencies.

Clone the ecommerce-demo repository using git:
```python
git clone 
```
Create a virtual environment to install dependencies in and activate it:
```python
python3 -m venv env
source env/bin/activate
```

Then install the dependencies:
```python
(env)$ pip install -r requirement.txt
```
Note the ```(env)``` in front of the prompt. This indicates that this terminal session operates in a virtual environment set up by virtualenv2.

Once ```pip``` has finished downloading the dependencies:
```python
(env)$ cd task_management
(env)$ python3 manage.py runserver
```
And navigate to ```http://127.0.0.1:8000/```


## Run test cases
in root folder (where the manage.py present) we can run individual apps (users,task,comments)
#### commands are in below
``` python manage.py test users ```,
``` python manage.py test tasks ```,
``` python manage.py test comments ```