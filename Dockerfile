FROM python:3.12-alpine

COPY requirements.txt /bot/
RUN pip install --no-cache-dir -r /bot/requirements.txt

COPY . /bot/

WORKDIR /bot/

CMD ["python3", "./main.py"]