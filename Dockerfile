FROM python:3.6
LABEL maintainer="An Bochuan <anbochuan@gmail.com>"

COPY /requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install Flask-SQLAlchemy
RUN pip3 install mysqlclient
RUN pip3 install pymysql
RUN pip3 install python-dotenv
RUN pip3 install pyjwt

# Default ENV variables
ENV DB_CONNECTION_STRING mysql+pymysql://root:auth@192.168.1.105:3306/authentication

COPY ./ /app/

EXPOSE 80

CMD ["python3", "main.py"]
