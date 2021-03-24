# pull official base image
FROM python:3.8-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# my env vars
ENV DJANGO_SECRET c76y8nc7o7nelf*1#dx=@90s62#ixlkj+u!=)&w50w2m$^ou7t
ENV POSTGRES_PASSWORD AsimovIsaac.73
ENV AZURE_STORAGE DefaultEndpointsProtocol=https;AccountName=spotifyhistory;AccountKey=DTUMCNrl9+TBIow20qe
ENV SPOTIFY_CLIENT_ID 9656ff22d7604d078e98e54a1870b92d
ENV SPOTIFY_CLIENT_SECRET fb911aa2dad04fd7be1754b2d94d0ac6


## install dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc && \
    apt-get clean

# install psycopg2 dependencies
RUN pip3 install numpy && \
    pip3 install pandas


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
