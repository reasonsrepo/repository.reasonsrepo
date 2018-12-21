'''
tamilrasigan deccandelight plugin
Copyright (C) 2017 Gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
from _base_ import Scraper
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib, re, requests, HTMLParser

class rasigan(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://tamilrasigan.net/'
        self.icon = self.ipath + 'rasigan.png'
        self.list = {'01Featured': self.bu[:-1],
                     '02New Releases': self.bu + 'tamil-movies-online/',
                     '03Super Hit Movies': self.bu + 'category/super-hit-movies/',
                     '04Trailers & Songs': self.bu + 'category/tamil-videos/',
                     '05[COLOR yellow]** Search **[/COLOR]': self.bu + '?s='}
    
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Tamil Rasigan')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        if '/tamil-movies-online/' in url:
            mlink = SoupStrainer('ul', {'class':'lcp_catlist'})
            mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
            items = mdiv.findAll('li')
        else:
            mlink = SoupStrainer('div', {'id':'content'})
            mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
            if url == self.bu[:-1]:
                items = mdiv.findAll('div', {'class':'awaken-block-post'})
            else:
                items = mdiv.findAll('article')

        for item in items:
            if '/tamil-movies-online/' in url:
                title = h.unescape(item.text)
            else:
                title = h.unescape(item.h1.text)
            title = self.clean_title(title)
            iurl = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            movies.append((title,thumb,iurl))
           
        if '/tamil-movies-online/' in url:   
            plink = SoupStrainer('ul', {'class':'lcp_paginator'})
        else:
            plink = SoupStrainer('nav', {'id':None})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        if '&gt;&gt;' in str(Paginator):
            currpg = Paginator.find('li', {'class':'lcp_currentpage'}).text
            pages = Paginator.findAll('li', {'class':None})
            lastpg = pages[len(pages)-2].text
            purl = pages[len(pages)-1].find('a')['href']
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        elif 'next' in str(Paginator):
            nlink = Paginator.find('a', {'class':re.compile('^next')})
            purl = nlink.get('href')
            currpg = Paginator.find('span', {'class':'page-numbers current'}).text
            pages = Paginator.findAll('a', {'class':'page-numbers'})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,iurl):
        videos = []
        html = requests.get(iurl, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'entry-content'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        links = videoclass.findAll('iframe')
        for link in links:
            url = link.get('src')
            self.resolve_media(url,videos)
            
        return videos