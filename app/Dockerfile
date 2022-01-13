FROM python

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip install uwsgi

COPY . /app

WORKDIR /app

CMD ["uwsgi","--ini", "/app/uwsgi.ini"]
# CMD ["python", "/app/main.py"]