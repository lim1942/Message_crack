from github import Github,ContentFile
from getpass import getpass
from queue import Queue
import logging
from .cloopen import Cloopen
import re
import codecs

client = Github(login_or_token='lim1940', password='21213121221', per_page=20)



def search_all(keyword, max_page=10, greenlet_count=4):
    """
    通过协程并发搜索
    :param max_page 最大页数
    :param greenlet_count 协程数量
    """
    accounts = set()
    with open('list.txt',encoding='utf-8') as f:
        contents = eval(f.read())
    for j,content in enumerate(contents):
        print (j)
        try:
            accounts.update({Cloopen(content[0],content[1],content[2])})
        except Exception as e:
            print(e)

    return accounts




