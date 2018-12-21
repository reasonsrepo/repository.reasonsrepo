'''
thiruttuvcd deccandelight plugin
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

class tvcd(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.thiruttuvcd.me/category/'
        self.icon = self.ipath + 'tvcd.png'
        self.list = {'01Tamil Movies': self.bu + 'tamil-movies-online/',
                     '02Malayalam Movies': self.bu + 'malayalam/',
                     '03Telugu Movies': self.bu + 'watch-telugu-movie/',
                     '04Hindi Movies': self.bu + 'hindi-movies-online/',
                     '05Tamil TV Shows': self.bu[:-9] + 'tv/',
                     '06[COLOR cyan]Adult Movies[/COLOR]': self.bu + 'hot-movies/',
                     '07[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}
    
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Thiruttu VCD')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'postcont'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'wp-pagenavi'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'class':'postbox'})
        
        for item in items:
            title = h.unescape(item.h2.text)
            title = self.clean_title(title)
            url = item.find('a')['href']
            thumb = item.find('img')['src'].encode('utf8')
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextli = Paginator.find('a', {'class':'nextpostslink'})
            purl = nextli.get('href')
            pgtxt = Paginator.find('span', {'class':'pages'}).text
            title = 'Next Page.. (Currently in %s)' % pgtxt
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':re.compile('^textsection')})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('a')			
            for link in links:
                strurl = link.get('href')
                self.resolve_media(strurl,videos)
        except:
            pass

        mlink = SoupStrainer('div', {'class':re.compile('^videosection')})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)                 
        try:
            links = videoclass.findAll('iframe')
            for link in links:
                strurl = link.get('data-lazy-src')
                self.resolve_media(strurl,videos)
        except:
            pass

        try:
            for link in links:
                strurl = link.get('src')
                self.resolve_media(strurl,videos)
        except:
            pass

        try:
            links = videoclass.findAll('a', {'type':'button'})
            for link in links:
                url = re.findall("(http.*?)'",link.get('onclick'))[0]
                if 'tv?vq=medium#/' in url:
                    url = url.replace('tv?vq=medium#/','')
                self.resolve_media(url,videos)
        except:
            pass
            
        return videos
