import client


if __name__ == '__main__':
    bot_client = client.RedmacBotClient('.token', 'rules.json')
    bot_token = bot_client.token
    bot_client.run(bot_token)
