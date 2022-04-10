# Backyard-coupe-managment-system

###[demo on heroku]( "https://obscure-sands-56196.herokuapp.com/flocks/")

An aplication to help with managment of your home hens flock, this fun project has been 
created to father improve my python, django, database, html, css, and docker skills. 
This project was also first that I have deployed to heroku through docker image

## Technologies
Application is created with:

* Python 3.8
* Django 4Screenshot from 2022-04-10 13-36-08
* Postgres
* Docker
* Docker-compose
 
## Setup
Requirements:
- Docker
- Docker-Compose
- Python 3.8

You need to have Docker and Docker-Compose on your devices.
Change .env-default to .env and edit with your settings

To run it use 
```docker-compose -d --build```
![Screenshot from 2022-04-10 13-36-08](https://user-images.githubusercontent.com/90859229/162616246-3b7a94b2-a233-4943-b79c-36f4653afea2.png)


## Use
you can log in as admin:
Admin panel: 'http://0.0.0.0:8000/admin/'
or create your own user following website instruction

When you are logged in you can add your own flock, feed, and records, 
app will add weather data for your flock location from open weather appi,
once you have some records you can check dashboard chart to see them.

##Run tests
```docker-compose run tests```

##Thanks for checking
Marcin Wlodarczyk
    
    - GitHub: https://github.com/gonzzur75
    - LinkedIn: www.linkedin.com/in/marcin-włodarczyk-bb58a9234
    - CodeWars: https://www.codewars.com/users/gonzur75

License
Copyright © 2022 MArcin Wlodarczyk.
This project is Beerware licensed.


