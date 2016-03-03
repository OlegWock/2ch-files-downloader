#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import requests as req
import os, sys, argparse


def getThreadNum(url):
    # domain, board, number
    return url.split("/")[-4], url.split("/")[-3], url.split("/")[-1].replace(".html", "")

parser = argparse.ArgumentParser(description='Files downloader from 2ch.hk by OlegWock v0.1')
parser.add_argument(action='store', dest='url', help='Thread url', default="", nargs='?')
parser.add_argument('-v', action='store_true', dest='v', help='Disable output')
args = parser.parse_args()
url = args.url

if not url:
    url = input("Enter thread url: ")
domain, b, n = getThreadNum(url)
folder = "{}_{}".format(b, n)

if not os.path.exists(folder) or not os.path.isdir(folder):
    os.mkdir(folder)

t = req.get("http://{domain}/makaba/mobile.fcgi?task=get_thread&board={board}&thread={thread}&post=1"
                                                    .format(domain=domain, board=b, thread=n)).json()

if "Error" in t:
    print("Error:", t["Error"])
    sys.exit(1)

for p in t:
    if "files" in p:
        for f in p['files']:
            if not args.v:
               print("Downloading file " + "http://{}/{}/{}".format(domain, b, f['path']))
            f_obj = req.get("http://{}/{}/{}".format(domain, b, f['path']))
            f_d = open("{}/{}".format(folder, f['name']), 'wb')
            f_d.write(f_obj.content)
            f_d.close()
            if not args.v:
                print("Done!~")
        if not args.v:
            print("="* 40)



