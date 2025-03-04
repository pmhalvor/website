FROM python:3.11-slim

WORKDIR /new_home

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY ./templates ./templates
COPY ./static ./static

EXPOSE 5001

ENV FLASK_ENV=production

CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:app"]