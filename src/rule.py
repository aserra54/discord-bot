import json
import logging
import os
import random


LOGGER = logging.getLogger('discord.redmac.rule')
LOGGER.setLevel(logging.DEBUG)


class Rules:
    '''Main entry point for processing a message. The constructor takes the path to the rules file for loading the
    rule definitions. Otherwise defines a single async 'handle' method, which takes in a Discord message and sends a
    response to it, if necessary.'''

    def __init__(self, path):
        self._rules = self._read_rules(path)

    def _read_rules(self, path):
        config = self._read_json(path)
        return self._parse_rules(config)

    def _read_json(self, path):
        if not os.path.isfile(path):
            raise ValueError(f'No such path: {path}')
        with open(path, 'r') as f:
            return json.loads(f.read())

    def _parse_rules(self, config):
        rules = []
        for rule_json in config['rules']:
            rule = Rule(rule_json)
            rules.append(rule)
        return rules

    async def handle(self, message):
        for rule in self._rules:
            if rule.should_apply(message):
                response = rule.get_response()
                self._log_match(message, rule, response)
                if response:
                    await message.channel.send(response)
                break

    def _log_match(self, message, rule, response):
        LOGGER.debug('Found match for message:')
        LOGGER.debug(f'   Category: {message.channel.category}')
        LOGGER.debug(f'   Channel:  {message.channel.name}')
        LOGGER.debug(f'   Author:   {message.author.name}')
        LOGGER.debug(f'   Message:  {message.content}')
        LOGGER.debug(f"   Response: {response if response else '<empty>'}")


class Rule:

    def __init__(self, rule_json):
        self._channel = rule_json.get('channel', None)
        self._rate = rule_json.get('rate', 1.0)
        self._authors = rule_json.get('authors', [])
        self._substrings = rule_json.get('contains', [])
        self._excludes = rule_json.get('not_contains', [])
        self._responses = rule_json.get('responses', [])
        self._validate()
    
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
