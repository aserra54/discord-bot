FROM python:3.12.1
WORKDIR /bot
COPY .token .
COPY src .
COPY data data
COPY etc etc
RUN pip install -r etc/requirements.txt
CMD python main.py
