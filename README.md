# Item List App

This is an app to exercise all the skills acquired till now with the Fullstack WebDeveloper Nanodegree.

This is a simple app which will let you access a list of Categories and Items from a Database. It will also let you add, edit and delete Items if you are previously authenticaded via Google Oauth.

To run this project on your enviroment there are some instructions related to the authentication with google, that will be thaught further in this doc. 

I hope you have a good time using the app, and if you have suggestions and fixes please feel free to open a PR. I will be totally gratefull!


## How to Configure your app
In order to run this app you're gonna have to have in your machine:
- Python 
- Flask
- SqlAlchemy
- Sqlite

- (and some libs related to the auth step)

After you have installed all the requirements, you should be able to run the app. 

1. The first step is to create your DataBase.
``` python models.py```

2. Populate the DB:
```python populatedb.py```

3. Then run the app:
``` python views.py```
