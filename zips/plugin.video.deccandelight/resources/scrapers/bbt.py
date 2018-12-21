'''
bigbosstamil deccandelight plugin
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

class bbt(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.bigbosstamil.net/'
        self.icon = self.ipath + 'bbt.png'
                  
    def get_menu(self):
        h = HTMLParser.HTMLParser()
        html = requests.get(self.bu, headers=self.hdr).text
        mlink = SoupStrainer('select', {'class':'postform'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('option', {'class':'level-0'})
        list = {}
        ino = 1
        for item in items:
            list['%03d%s'%(ino,h.unescape(item.text))]= self.bu + '?cat=%s'%item.get('value')
            ino+=1
        list['999[COLOR yellow]** Search **[/COLOR]']= self.bu + '?s='
        return (list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('BigBoss Tamil')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('ul', {'class':re.compile('^listing-videos')})
        plink = SoupStrainer('div', {'class':'pagination'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('li')
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        for item in items:
            title = h.unescape(item.text)
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            movies.append((title, thumb, url))

        if 'Next' in str(Paginator):
            nextli = Paginator.find('a', {'class':re.compile('^next')})
            purl = nextli.get('href')
            currpg = Paginator.find('span').text
            lastpg = Paginator.findAll('a', {'class':'page-numbers'})[-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('iframe')
        links = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            for link in links:
                vidurl = link.get('src')
                self.resolve_media(vidurl,videos)
        except:
            pass
            
        return videos
