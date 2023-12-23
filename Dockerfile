FROM python:3.12.1
WORKDIR /bot
COPY . .
RUN ls /
CMD ls /
