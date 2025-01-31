FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .

RUN python3 -m pip install --upgrade pip && pip3 install --no-cache --upgrade -r requirements.txt

WORKDIR /home/app

COPY . .

CMD ["python3", "main.py"]
