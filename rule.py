import configparser
import os
import random


class Rules:
    '''Main entry point for processing a message. The constructor takes the path to the rules file for loading the
    rule definitions. Otherwise defines a single async 'handle' method, which takes in a Discord message and sends a
    response to it, if necessary.'''

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
        self._excludes = []
        self._responses = []

        self._parse_section(section)
        self._validate()

    def _parse_section(self, section):
        for key, value in section.items():
            if key == 'channel':
                self._channel = value
            elif key == 'rate':
                self._rate = float(value)
            elif key.startswith('author'):
                self._authors.append(value)
            elif key.startswith('contains'):
                self._substrings.append(value)
            elif key.startswith('not_contains'):
                self._excludes.append(value)
            elif key.startswith('response'):
                self._responses.append(value)
    
    def _validate(self):
        if self._channel is None:
            raise Exception('No channel specified')
        if len(self._responses) == 0:
            raise Exception('Rule has no responses')
        if len(self._authors) == 0 and len(self._substrings) == 0 and len(self._excludes) == 0:
            raise Exception('Rule has no definitions')

    def should_apply(self, message):
        if message.channel.name != self._channel:
            return False
        if len(self._authors) > 0 and message.author.name not in self._authors:
            return False
        content = message.content.lower()
        for substring in self._substrings:
            if substring not in content:
                return False
        for exclude in self._excludes:
            if exclude in content:
                return False
        return True

    def get_response(self):
        if random.random() < self._rate:
            return random.choice(self._responses)
        return ''
