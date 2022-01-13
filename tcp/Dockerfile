FROM python

ENV TZ=Asia/Shanghai

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /tcp

CMD [ "python","/tcp/tcp.py" ]