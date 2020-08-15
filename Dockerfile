FROM python:3.8.1

# Set environment variables
ENV PYTHONUNBUFFERED 1


RUN mkdir /code 
WORKDIR /code/ 
ADD . /code/ 

RUN pip install -U pip 

# NOTE -- need to individually install private repos from a private .env file... 
RUN pip install -r requirements-dev.txt 
EXPOSE 8000 8001
