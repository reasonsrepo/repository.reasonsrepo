'''
tamilserialtoday247 deccandelight plugin
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

class tst247(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.tamilserialtoday247.net/'
        self.icon = self.ipath + 'tst247.png'
                     
    def get_menu(self):
        h = HTMLParser.HTMLParser()
        r = requests.get(self.bu, headers=self.hdr)
        if r.url != self.bu:
            self.bu = r.url
        items = {}
        cats = re.findall('id="menu-item-(?!19104|7|362).+?href="([^"]+)">([^<]+)',r.text)
        sno = 1
        for url,title in cats:
            items['%02d'%sno+h.unescape(title).encode('utf8')] = url
            sno+=1
        items['99[COLOR yellow]** Search **[/COLOR]'] = self.bu + '/?s='
        return (items,7,self.icon)
        
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        episodes = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Tamil Serial Today')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('ul', {'class':re.compile('^listing-videos')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'pagination'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('li')
        
        for item in items:
            try:
                title = h.unescape(item.text)
            except:
                title = h.unescape(item.find('a')['title'])
            try:
                title = re.findall('(.+?\d{2}-*\d{2}-*\d{4})',title)[0]
            except:
                pass
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            episodes.append((title, thumb, url))
        
        if 'Next' in str(Paginator):
            pgtxt = Paginator.span.text
            purl = Paginator.findAll('a')[-2].get('href')
            title = 'Next Page.. (Currently in %s)' % pgtxt
            episodes.append((title, self.nicon, purl))
        
        return (episodes,8)

    def get_videos(self,url):
        videos = []
        h = HTMLParser.HTMLParser()    
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'video-embed'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
          
        try:
            links = videoclass.findAll('iframe')
            for link in links:
                vidurl = link.get('src').strip()
                self.resolve_media(vidurl,videos)
        except:
            pass
            
        return videos
