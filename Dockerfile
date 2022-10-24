# pull official base image
FROM python:3.9.6-alpine

ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk update \
    && apk add zlib-dev jpeg-dev gcc musl-dev
    #&& apk add python3-dev py3-setuptools \
    #&& apk add tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    #libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    #libxcb-dev libpng-dev

 #libjpeg-dev zlib1g-dev
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
#COPY entry.sh .
#RUN sed -i 's/\r$//g' /usr/src/app/entry.sh


# copy project
COPY . .
RUN chmod +x /usr/src/app/entry.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entry.sh"]