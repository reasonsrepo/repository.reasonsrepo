import os
import urllib, urllib2
import urlparse

import requests

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.74 Safari/537.36'}

def http_get(url, headers=None, cook=None):
    try:
        r = requests.get(url, headers=headers, cookies=cook).content
        return r
    except urllib2.URLError, e:
        return ''

def http_post(url, cookie_file='', postData={}, data=''):
    try:
        if (data != ''):
            postData = dict(urlparse.parse_qsl(data))
        net = Net(cookie_file=cookie_file)
        return net.http_POST(url,postData).content
    except urllib2.URLError, e:
        return ''
