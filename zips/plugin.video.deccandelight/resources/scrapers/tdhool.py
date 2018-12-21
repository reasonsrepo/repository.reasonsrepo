'''
tamildhool deccandelight plugin
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

class tdhool(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.tamildhool.com/'
        self.icon = self.ipath + 'tdhool.png'
        self.list = {'01Sun TV': self.bu + 'sun-tv-programs/MMMM5',
                     '02Vijay TV': self.bu + 'vijay-tv-programs/MMMM5',
                     '03Zee Tamil TV': self.bu + 'zee-tamil-programs/MMMM5',
                     '04Colors Tamil TV': self.bu + 'colors-tamil/',
                     '05Raj TV': self.bu + 'raj-tv/',
                     '06Polimer TV': self.bu + 'polimer-tv/',
                     '07Jaya TV': self.bu + 'jaya-tv/',
                     '08News & Gossips': self.bu + 'news-gossips/',
                     '09Tamil TV Programs': self.bu + 'tamil-tv/',
                     '99[COLOR yellow]** Search **[/COLOR]': self.bu + '?s='}
                     
    def get_menu(self):
        return (self.list,7,self.icon)

    def get_second(self,iurl):
        """
        Get the list of shows.
        :return: list
        """
        shows = []
        h = HTMLParser.HTMLParser()
        html = requests.get(iurl, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'wc-gallery'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('div', {'class':'gallery-item'})
        for item in items:
            title = h.unescape(item.text)
            url = item.find('a')['href']
            try:
                icon = item.find('img')['src']
            except:
                icon = self.icon
            
            shows.append((title,icon,url)) 
        
        return (shows,7)
        
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        episodes = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Tamil Dhool')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('main', {'id':'main'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'navigation'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('article')
        
        for item in items:
            try:
                title = h.unescape(item.h3.text)
            except:
                title = h.unescape(item.find('a')['title'])
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            episodes.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextli = Paginator.find('a', {'class':re.compile('^next')})
            purl = nextli.get('href')
            currpg = Paginator.find('span').text
            lastpg = Paginator.findAll('a', {'class':'page-numbers'})[-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            episodes.append((title, self.nicon, purl))
        
        return (episodes,8)

    def get_videos(self,url):
        videos = []
        h = HTMLParser.HTMLParser()    
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'content-area'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('video')
            for link in links:
                vidurl = link.find('source')['src']
                self.resolve_media(vidurl,videos)
        except:
            pass

        try:
            links = videoclass.findAll('noscript')
            for link in links:
                vidurl = link.find('iframe')['src'].strip()
                self.resolve_media(vidurl,videos)
        except:
            pass
            
        try:
            if 'noscript' not in str(videoclass):
                links = videoclass.findAll('iframe')
                for link in links:
                    vidurl = link.get('src').strip()
                    self.resolve_media(vidurl,videos)
        except:
            pass
            
        return videos
