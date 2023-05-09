FROM python:3.11

WORKDIR /home/app/lf_campus

COPY ./requirements.txt /requirements.txt

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        gdal-bin \
        libgdal-dev \
        python3-gdal \
        libgeos-dev \
        libproj-dev \
    && pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD["python3", "manage.py", "runserver", "0.0.0.0:8000"]
