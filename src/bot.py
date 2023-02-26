import client
import os


def read_token(token_path):
    if not os.path.isfile(token_path):
        raise ValueError(f'No such file: {token_path}')
    with open(token_path, 'r') as f:
        return f.read()


def main():
    token = read_token('.token')
    bot_client = client.RedmacBotClient('rules.json')
    bot_client.run(token)


if __name__ == '__main__':
    main()
