'''
abcmalayalam deccandelight plugin
Copyright (C) 2016 Gujal

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
import urllib, re, requests
import HTMLParser
from resources.lib import cfscrape
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("torm", 1)

class torm(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'https://www.tormalayalam.com'
        self.icon = self.ipath + 'torm.png'
        self.list = {'01Movies': self.bu + '/movies'}

    def get_cfpass(self):
        durl = self.bu + '/components/com_k2/images/ratingstars.gif'
        cj = cfscrape.get_tokens(durl,user_agent=self.hdr['User-Agent'])[0]
        ckstr = '; '.join([str(x)+"="+str(y) for x,y in cj.items()])
        return (cj,ckstr)
        
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        cj,ckstr = cache.cacheFunction(self.get_cfpass)
        h = HTMLParser.HTMLParser()
        movies = []

        html = requests.get(url, headers=self.hdr, cookies=cj).text
        mlink = SoupStrainer('div', {'class':'itemList'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'k2Pagination'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('span', {'class':'catItemImage'})
        
        for item in items:
            title = h.unescape(item.find('a')['title']).encode('utf8')
            #title = self.clean_title(title)
            url = self.bu + item.find('a')['href']
            thumb = self.bu + item.find('img')['src'] + '|User-Agent=%s&Cookie=%s'%(self.hdr['User-Agent'],ckstr)
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            pdiv = Paginator.find('a', {'class':'next'})
            purl = self.bu + pdiv.get('href')
            pgtxt = re.findall('(Page\s[^<]+)',Paginator.text)[0].strip()
            title = 'Next Page.. (Currently in %s)' % pgtxt
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        cj,ckstr = cache.cacheFunction(self.get_cfpass)
        videos = []
            
        html = requests.get(url, headers=self.hdr, cookies=cj).text
        mlink = SoupStrainer('div', {'class':'itemFullText'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            vidurl = re.findall('Watch Online:.+?href="([^"]+)',html,re.DOTALL)[0]
            self.resolve_media(vidurl,videos)
        except:
            pass
            
        try:
            links = videoclass.findAll('div', {'class':'avPlayerContainer'})
            for link in links:
                vidurl = link.find('iframe')['src']
                if 'http' not in vidurl:
                    vidurl = 'http:' + vidurl
                self.resolve_media(vidurl,videos)
        except:
            pass

        try:
            table = videoclass.find('div', {'class':'divTable'})
            links = table.findAll('a')
            for link in links:
                vidurl = link.get('href')
                self.resolve_media(vidurl,videos)
        except:
            pass

        try:
            table = videoclass.find('table')
            links = table.findAll('a')
            for link in links:
                vidurl = link.get('href')
                self.resolve_media(vidurl,videos)
        except:
            pass
      
        return videos
