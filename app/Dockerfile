#Base Image
FROM python:3.8
# root
WORKDIR /app

#set default enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
#install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#copy project
COPY . /app
# collect static files
CMD python manage.py collectstatic --noinput
CMD python manage.py makemigrations && python manage.py migrate
#

#run gunicorn
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT