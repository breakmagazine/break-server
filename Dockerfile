FROM python:3.9.12

RUN apt-get update && apt-get install -y python3-pip && apt-get clean

WORKDIR /break-server/
ADD . /break-server/
RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt
RUN python manage.py makemigrations