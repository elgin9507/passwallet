FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV APP_ROOT /passwallet

WORKDIR ${APP_ROOT}

COPY . ${APP_ROOT}

RUN pip install -U pip
RUN pip install -r requirements.txt

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
