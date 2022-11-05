FROM python:3.10.8

WORKDIR /code
EXPOSE 5000

COPY ./src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD PYTHONPATH=. python api/app.py