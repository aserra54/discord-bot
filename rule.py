import configparser
import os
import random


class Rules:

    def __init__(self, path):
        self._rules = self._read_rules(path)

    def _read_rules(self, path):
        config = self._read_config(path)
        return self._parse_rules(config)

    def _read_config(self, path):
        if not os.path.isfile(path):
            raise ValueError(f'No such path: {path}')
        config = configparser.ConfigParser()
        config.read(path)
        return config

    def _parse_rules(self, config):
        rules = []
        for section_name in config.sections():
            if section_name.startswith('Rule'):
                section = config[section_name]
                rule = Rule(section)
                rules.append(rule)
        return rules

    async def handle(self, message):
        for rule in self._rules:
            if rule.should_apply(message):
                response = rule.get_response()
                if response:
                    await message.channel.send(response)
                break


class Rule:

    def __init__(self, section):

        self._channel = None
        self._rate = 1.0
        self._authors = []
        self._substrings = []
        self._responses = []

        for key, value in section.items():
            if key == 'channel':
                self._channel = value
            elif key == 'rate':
                self._rate = float(value)
            elif key.startswith('author'):
                self._authors.append(value)
            elif key.startswith('contains'):
                self._substrings.append(value)
            elif key.startswith('response'):
                self._responses.append(value)
        
        if self._channel is None:
            raise Exception('No channel specified')
        if len(self._responses) == 0:
            raise Exception('Rule has no responses')
        if len(self._authors) == 0 and len(self._substrings) == 0:
            raise Exception('Rule has no definitions')

    def should_apply(self, message):
        if message.channel.name != self._channel:
            return False
        if len(self._authors) > 0 and message.author.name not in self._authors:
            return False
        for substring in self._substrings:
            if substring not in message.content.lower():
                return False
        return True

    def get_response(self):
        if random.random() < self._rate:
            return random.choice(self._responses)
        return ''