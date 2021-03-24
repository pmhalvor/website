
# official base image
FROM python:3.8-alpine

# set work directory
WORKDIR /site

# set environment variables
ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SECRET c76y8nc7o7nelf*1#dx=@90s62#ixlkj+u!=)&w50w2m$^ou7t
ENV POSTGRES_PASSWORD AsimovIsaac.73
ENV AZURE_STORAGE DefaultEndpointsProtocol=https;AccountName=spotifyhistory;AccountKey=DTUMCNrl9+TBIow20qe
ENV SPOTIFY_CLIENT_ID 9656ff22d7604d078e98e54a1870b92d
ENV SPOTIFY_CLIENT_SECRET fb911aa2dad04fd7be1754b2d94d0ac6
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev \
    && apk add gcc \
    && apk add python3-dev \
    && apk add musl-dev 

# other install necessary
RUN apk add libffi-dev
 
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
# needs to be installed before pandas (for some reason?)
RUN pip install numpy 
RUN pip install -r requirements.txt 

# copy project
COPY . .

