FROM python:3.10.12-alpine

WORKDIR /app

COPY req.txt r.txt

RUN pip install --upgrade pip
RUN pip install -r r.txt


COPY . .

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
