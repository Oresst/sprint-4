FROM python:3.8

RUN apt update

WORKDIR /sprint-4

COPY req.txt req.txt

RUN  pip install --upgrade pip \
     && pip install -r req.txt --no-cache-dir

COPY . .

# Укажите, как запускать ваш сервис
CMD ["python3", "src/main.py"]
