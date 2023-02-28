import bot
import logging
import os


def setup_logging():
    log_level = logging.INFO
    log_format = '%(asctime)s | %(levelname)-7s | [%(name)s] %(message)s'
    logging.basicConfig(level=log_level, format=log_format)


def read_token(token_path):
    if not os.path.isfile(token_path):
        raise ValueError(f'No such file: {token_path}')
    with open(token_path, 'r') as f:
        return f.read()


def main():
    setup_logging()
    token = read_token('.token')
    redmac_bot = bot.RedmacBot('rules.json')
    redmac_bot.run(token)


if __name__ == '__main__':
    main()
