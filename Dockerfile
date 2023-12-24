FROM python:3.12.1
WORKDIR /bot
COPY .token .
COPY src/*.py ./
COPY src/util/*.py ./util/
COPY etc/* ./
RUN pip install -r requirements.txt
CMD python main.py
