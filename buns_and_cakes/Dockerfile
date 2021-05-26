# pull official base image
FROM python:3.9.0
# set work directory
WORKDIR /usr/src/buns_and_cakes
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
# copy project
COPY . .
CMD ["python", "main.py"]