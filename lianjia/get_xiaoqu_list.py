#!/usr/bin/env python
# coding: utf8

import multiprocessing
import re
import os

import requests
import bs4

ROOT_URL = "http://bj.lianjia.com/xiaoqu/"
FILE = "all_xiaoqu.txt"


def get_all_url():
    all_url = []
    for i in xrange(1, 101):
        all_url.append(ROOT_URL + "pg" + str(i) + "/")

    return all_url


def generate_info(text, lock):
    info = {}
    tag = bs4.BeautifulSoup(text, "lxml")

    info["id"] = tag.a["href"].lstrip(ROOT_URL).strip("/")
    print(info["id"])
    info["title"] = tag.select_one(".title").a.string.encode("utf8")
    print (info["title"])
    other = tag.select_one(".positionInfo")
    info["info"] = u" ".join([tag.select_one(".totalPrice").span.string + u"\u5143/m2"] +
                            [i.string for i in other.select("a")] + 
                            [other.select_one("a").nextSibling.nextSibling.nextSibling]).encode("utf8")
    print(info["info"])
    url = ROOT_URL + info["id"] + "/"
    response = requests.get(url)
    response.encoding = "utf8"

    try:
        a = bs4.BeautifulSoup(response.text, "lxml")\
                .select_one(".averagePriceCard.xiaoquPriceCard.fr")
        if a.find(text=re.compile(u"\xa0\u540c\u6bd4\u53bb\u5e74\u4e0a\u6da8")):
            info["rate"] = a.find(text=re.compile(u"\xa0\u540c\u6bd4\u53bb\u5e74\u4e0a\u6da8")).nextSibling.string.encode("utf8")
        elif a.find(text=re.compile(u"\xa0\u540c\u6bd4\u53bb\u5e74\u4e0b\u964d")):
            info["rate"] = (u"-" + a.find(text=re.compile(u"\xa0\u540c\u6bd4\u53bb\u5e74\u4e0b\u964d")).nextSibling.string).encode("utf8")
        else:
            info["rate"] = u"0.00%".encode("utf8")
    except:
        info["rate"] = u"0.00%".encode("utf8")
    print(info["rate"])

    with lock:
        with open(FILE, "a") as f:
            f.write("{title} {rate} {info}\n".format(
                title=info["title"], rate=info["rate"], info=info["info"]))

    return info


def main():
    if os.path.isfile(FILE):
        os.remove(FILE)

    manager = multiprocessing.Manager()
    lock = manager.Lock()
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() * 2)

    for url in get_all_url():
        response = requests.get(url)
        response.encoding = "utf8"
        soup = bs4.BeautifulSoup(response.text, "lxml")
        for i in soup.select_one(".listContent").select(".clear"):
            pool.apply_async(generate_info, (str(i), lock))

    pool.close()
    pool.join()


if __name__ == "__main__":
    main()
