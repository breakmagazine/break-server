FROM python:3.9.12
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y vim && apt-get clean

RUN mkdir /srv/docker-server
ADD . /srv/docker-server

WORKDIR /srv/docker-server

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]