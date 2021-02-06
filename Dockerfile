FROM python:3.7.2-alpine3.8
COPY . .

RUN pip install -r  ./requirements.txt 

EXPOSE 5000
ENTRYPOINT ["python", "./app.py"]
