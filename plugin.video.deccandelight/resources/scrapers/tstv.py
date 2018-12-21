'''
tamilserials deccandelight plugin
Copyright (C) 2018 Gujal

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

class tstv(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.tamilserials.tv/category/'
        self.icon = self.ipath + 'tstv.png'
        self.list = {'01Sun TV': self.bu + 'sun-tv-serials/',
                     '02Vijay TV': self.bu + 'vijay-tv-serials/',
                     '03Zee Tamil TV': self.bu + 'zee-tamil-serials/',
                     '04Polimer TV Serials': self.bu + 'polimer-tv-serials/',
                     '05Jaya TV': self.bu + 'jaya-tv/',
                     '06Kalaignar TV': self.bu + 'kalaignar-tv/',
                     '07Vendhar TV': self.bu + 'vendhar-tv/',
                     '08Puthuyugam TV': self.bu + 'puthu-yugam-tv/',
                     '09Other TV Shows': self.bu + 'tv-shows/',
                     '10Short Films': self.bu + 'tamil-short-films/MMMM7',
                     '99[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s=MMMM7'}
            
    def get_menu(self):
        return (self.list,5,self.icon)

    def get_second(self,iurl):
        """
        Get the list of shows.
        :return: list
        """
        shows = []
        h = HTMLParser.HTMLParser()

        html = requests.get(iurl, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':re.compile('columns large-12')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('article')
        for item in items:
            title = h.unescape(item.a.text) + ' [%s]'%item.span.text
            tlink = item.find('div', {'class':'bg-pic'}).get('style')
            thumb = re.findall("url\('([^']+)",tlink)[0]
            url = item.find('a')['href']
            shows.append((title,thumb,url))
        return (shows,7)
        
    def get_items(self,iurl):
        episodes = []
        h = HTMLParser.HTMLParser()
        if iurl[-3:] == '?s=':
            search_text = self.get_SearchQuery('Tamil Serials')
            search_text = urllib.quote_plus(search_text)
            iurl += search_text
        html = requests.get(iurl).text
        mlink = SoupStrainer('div', {'class':re.compile('columns large-12')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('article')

        for item in items:
            title = h.unescape(item.a.text).encode('utf8')
            tlink = item.find('div', {'class':'bg-pic'}).get('style')
            thumb = re.findall("url\('([^']+)",tlink)[0]
            url = item.find('a')['href']         
            episodes.append((title,thumb,url))

        plink = SoupStrainer('div', {'class':'pagination-centered'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)

        if 'next page' in str(Paginator):
            currpg = Paginator.find('span', {'class':re.compile('current')}).text
            purl = Paginator.find('a', {'class':re.compile('next')}).get('href')
            lastpg = Paginator.findAll('a', {'class':re.compile('^page-numbers')})[-1].text
            title = 'Next Page.. (Currently in Page %s of %s)'%(currpg,lastpg)
            episodes.append((title, self.nicon, purl))
        return (episodes,8) 

    def get_videos(self,iurl):
        videos = []
        h = HTMLParser.HTMLParser()
        html = requests.get(iurl).text
        mlink = SoupStrainer('div', {'class':'entry-content'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
        try:
            items = videoclass.findAll('iframe')
            for item in items:
                vidurl = item['src']
                self.resolve_media(vidurl,videos)
        except:
            pass
        try:
            items = videoclass.findAll('figure')
            for item in items:
                vidurl = item.find('a')['href']
                self.resolve_media(vidurl,videos)
        except:
            pass
        
        return videos
