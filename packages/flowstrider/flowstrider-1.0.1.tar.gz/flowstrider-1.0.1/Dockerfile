FROM python:3.12

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y graphviz
RUN pip install .

ENTRYPOINT [ "flowstrider"]
