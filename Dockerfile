FROM python:3.12.1
WORKDIR /bot
COPY .token .
COPY src .
COPY data data
COPY etc .
RUN pip install -r requirements.txt
CMD python main.py
