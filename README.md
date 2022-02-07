## FastAPI_task

# How to run locally
- Project was implemented using `python3.8`
- Create your virtual environment
- Install dependencies: `pip install -r requirements.txt`
- Create your config.py file
- Create the database: `docker-compose -f docker-compose.dev.yaml up`
- Run local server: `python main.py`

# Object of this task
```
Object of this task is to create a simple REST API. You can use one framework from this list 
(Django Rest Framework, Flask or FastAPI) and all libraries which you prefer to use with 
this frameworks.
```
``` 
Basic models:
● User
● Post (always made by a user)
```
- `User` model is implemented in `apps.authorization` app
- `Post` model is implemented in `apps.posts` app
- `Like` model was created on my initiative. It is used to save likes of specific post
```
Basic Features:
● user signup
● user login
● post creation
● post like
● post unlike
● analytics about how many likes was made. Example url 
/api/analitics/?date_from=2020-02-02&date_to=2020-02-15 . API should return analytics 
aggregated by day.
● user activity an endpoint which will show when user was login last time and when he 
mades a last request to the service.
```

# Requirements
```
Requirements:
● Implement token authentication (JWT is prefered)
```
