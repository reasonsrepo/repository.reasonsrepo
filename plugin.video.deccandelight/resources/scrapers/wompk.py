'''
watchonlinemovies deccandelight plugin
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
import urllib, requests
import HTMLParser

class wompk(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.watchonlinemovies.com.pk/category/'
        self.icon = self.ipath + 'wompk.png'
        self.list = {'01Hindi Movies': self.bu + 'indian-movies/',
                     '02Dubbed Movies': self.bu + 'watch-hindi-dubbed-full-movies/',
                     '03Punjabi Movies': self.bu + 'watch-punjabi-movies-online/',
                     '04English Movies': self.bu + 'english-movies-free/',
                     '05[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}
                  
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('WOM PK')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'postbox'})
        plink = SoupStrainer('div', {'class':'wp-pagenavi'})
        items = BeautifulSoup(html, parseOnlyThese=mlink)
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        for item in items:
            title = h.unescape(item.find('img')['alt'])
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            movies.append((title, thumb, url))

        if 'nextpostslink' in str(Paginator):
            nextli = Paginator.find('a', {'class':'nextpostslink'})
            purl = nextli.get('href')
            pgtxt = Paginator.find('span', {'class':'pages'}).text
            title = 'Next Page.. (Currently in %s)' % pgtxt
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
