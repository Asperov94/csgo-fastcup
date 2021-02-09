FROM python:3.7.2-alpine3.8
WORKDIR /usr/src/app
RUN apk update
RUN apk add firefox-esr
RUN apk add xvfb
#RUN apk add xserver-xephyr
#RUN apk add vnc4server
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python", "-u", "./app.py"]
