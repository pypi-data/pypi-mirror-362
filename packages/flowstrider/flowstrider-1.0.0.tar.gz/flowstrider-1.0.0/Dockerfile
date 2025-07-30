FROM python:3.12

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y graphviz
RUN pip install -e .

ENTRYPOINT [ "python3", "src/flowstrider/tool.py"]
