FROM python:3.9

RUN mkdir -p /opt/application/flask
COPY requirements.txt /opt/application/flask
WORKDIR /opt/application/flask

RUN apt-get update
RUN pip install -r requirements.txt
ENV DATABASE_HOST postgres-db
EXPOSE 8088

ENTRYPOINT ["gunicorn", "-b", ":8088"]
CMD ["project.app:create_app()"]
