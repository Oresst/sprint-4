FROM python:3.8

ARG WD=/sprint-4
ARG GROUP=sprint4
ARG USER=fastapi

WORKDIR $WD

RUN groupadd -r $GROUP \
    && useradd -d $WD -r -g $GROUP $USER \
    && chown $USER:$GROUP -R $WD \
    && chown $USER:$GROUP /var/log

COPY --chown=$USER:$GROUP requirements.txt requirements.txt

RUN apt update

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY --chown=$USER:$GROUP . .

# Укажите, как запускать ваш сервис
ENTRYPOINT ["python3", "src/main.py"]