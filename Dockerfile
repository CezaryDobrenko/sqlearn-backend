FROM python:3.9.7

WORKDIR /code
EXPOSE 5000

COPY ./src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD PYTHONPATH=. python api/app.py