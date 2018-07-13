import time
import re
import math
from gevent import monkey,pool
monkey.patch_all()
from github import Github,ContentFile


accounts = set()
_pool = pool.Pool(3)
client = Github(login_or_token='lim1942', password='helin05564880960', per_page=20)
language = ['php','java','python','ini','text','xml','javascript','objective-c','html','c#'] 



def extract(content):

    def search_field(keyword_and_pattern):
        keyword, pattern = keyword_and_pattern
        for line in content.split('\n'):
            if re.search(keyword, line, re.IGNORECASE):
                match = re.search(pattern, line)
                if match:
                    return match.group(0)

    account_sid, account_token, appid = map(search_field, [('sid', '[a-z0-9]{32}'),
                                                           ('token', '[a-z0-9]{32}'),
                                                           ('app.?id', '[a-z0-9]{32}')])
    if all([account_sid, account_token, appid]):
        return account_sid, account_token, appid


def search(l,key='app.cloopen.com'):

    search_line = key+'+language:'+l
    paging = client.search_code(search_line)
    total_page = min(20, math.ceil(paging.totalCount/50))
    for i in range(1, total_page+1):
        _pool.spawn(inner_search,paging,i,total_page,l)


def inner_search(paging,i,total_page,l):
    print(l +': '+str(i)+'/'+str(total_page))
    contents = map(lambda x: x.decoded_content.decode('utf-8'), paging.get_page(i))
    accounts.update({p for p in map(extract, contents) if p})


def main():
    l = language[3]
    search(l)
    try:
        with open ('list.txt') as f:
            con = eval(f.read())
    except:
        con = []

    content = list(accounts)
    print(l+': '+str(len(content))+'   total: '+str(len(con)))

    with open('list.txt','w') as f:
        for i in content:
            if i not in con:
                con.append(i)
        f.write(str(con))


def get_list_len():
    try:
        with open ('list.txt') as f:
            con = eval(f.read())
            print(len(con))
    except:
        con = []



if __name__ == '__main__':
    main()
    get_list_len()