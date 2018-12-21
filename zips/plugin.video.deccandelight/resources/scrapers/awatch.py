'''
AndhraWatch DeccanDelight plugin
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
import urllib, re, requests
import HTMLParser

class awatch(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.andhrawatch.com/'
        self.icon = self.ipath + 'awatch.png'
        self.list = {'01Movies': self.bu + 'telugu-movies/',
                     '02Trailers': self.bu + 'movie-trailers/',
                     '03Short Films': self.bu + 'short-films/'}

    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':re.compile('^row ')})
        plink = SoupStrainer('nav', {'class':'herald-pagination'})
        
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('article')

        for item in items:
            title = h.unescape(item.text)
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src'].split('?')[0]
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
 
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        if 'Next' in str(Paginator):
            currpg = Paginator.find('span', {'class':re.compile('current')}).text
            purl = Paginator.find('a', {'class':re.compile('next')}).get('href')
            pages = Paginator.findAll('a', {'class':'page-numbers'})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in %s of %s)'%(currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,9)

    def get_video(self,url):
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('iframe')
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            vidurl = videoclass.find('iframe')['src'].split('?')[0]
        except:
            vidurl = None
      
        return vidurl
