FROM python:3.7-alpine

COPY requirements.txt /tmp

COPY email_app.py /app/
COPY log.json /app/ 

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY tracker.py /app/

WORKDIR /app
CMD ["python3", "tracker.py"]
