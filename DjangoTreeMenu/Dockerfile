FROM python:3.13.3-bookworm

WORKDIR /menu

COPY requirements.txt /menu/

RUN apt clean -y
RUN apt update -y
RUN apt install dos2unix -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . /menu/

RUN chmod u+x /menu/entrypoint.sh
RUN dos2unix /menu/entrypoint.sh

CMD ["./entrypoint.sh"]
