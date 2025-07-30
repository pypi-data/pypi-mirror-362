# -*- encoding: utf-8 -*-

'''
@File    :   md5_crack_helper.py
@Time    :   2025/07/16 12:12:42
@Author  :   test233
@Version :   1.0
'''

import re
import requests

requests.packages.urllib3.disable_warnings()


def cmd5_com(hash):
    session = requests.Session()
    r1 = session.get('https://cmd5.com/', verify=False)
    data = dict(re.findall(
        "<input.*name=\"(.*?)\".*value=\"(.*?)\".*/>", r1.text))
    data['ctl00$ContentPlaceHolder1$TextBoxInput'] = hash
    headers = {'Referer': 'https://cmd5.com/'}
    r2 = requests.post('https://cmd5.com/', headers=headers,
                       data=data, verify=False)
    return re.search(r"id=\"LabelAnswer\".*?>(.*?)<", r2.text).group(1) if re.search(r"id=\"LabelAnswer\".*?>(.*?)<", r2.text) else ''

def www_xmd5_com(hash):
    session = requests.Session()
    headers = {
        'Host': 'www.xmd5.com',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    r1 = session.get('http://www.xmd5.com/', headers=headers, verify=False)

    params = dict(re.findall("<input.*name=\"(.*?)\".*value=\"(.*?)\".*/>",r1.text))
    params['hash'] = hash
    params['xmd5'] = 'MD5 解密'
    params['open'] = 'on'

    
    r2 = session.get(
        'http://www.xmd5.com/md5/search.asp',
        params=params,
        headers=headers,
        verify=False,
    )
    r2.encoding = r2.apparent_encoding
    return re.search('Result:</font><font.*?>\s*?(.*?)\s*?</font>',r2.text,re.S).group(1) if re.search('Result:</font><font.*?>\s*?(.*?)\s*?</font>',r2.text,re.S) else ''

def md5_crack(hash):
    APIS = {
        # 'https://cmd5.com': cmd5_com,
        "http://www.xmd5.com": www_xmd5_com,
    }
    result = []
    for url, func in APIS.items():
        try:
            res = func(hash)
        except Exception as e:
            ret = str(e)
        result.append([url, res])
    return result


if __name__ == "__main__":
    hash = "21232f297a57a5a743894a0e4a801fc3"
    print(md5_crack(hash))
