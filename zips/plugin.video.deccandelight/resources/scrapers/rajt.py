'''
rajtamil deccandelight plugin
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
import urllib, requests, re

class rajt(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.icon = self.ipath + 'rajt.png'
        self.bu = 'http://www.rajtamil.com/category/'
        self.list = {'01Recent Movies': self.bu + 'movies/',
                     '02Dubbed Movies': self.bu + 'tamil-dubbed/',
                     '03Comedy Scenes': self.bu + 'comedy/',
                     '04Movie Songs': self.bu + 'download-songs/',
                     '05Sun TV Shows': self.bu + 'sun-tv-show/',
                     '06Vijay TV Shows': self.bu + 'vijay-tv-shows/',
                     '07[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}
    
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Raj Tamil')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer("li", {"id":re.compile('^post')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer("div", {"class":"navigation"})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('li')
        for item in items:
            title = item.find('a')['title']
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.img.get('src')
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextpg = Paginator.find('a', {'class':'next page-numbers'})
            purl = nextpg.get('href')
            currpg = Paginator.find('span', {'class':'page-numbers current'}).text
            pages = Paginator.findAll('a', {'class':'page-numbers'})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'entry-content'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('iframe')
            for link in links:
                url = link.get('src')
                self.resolve_media(url,videos)
        except:
            pass

        try:
            links = videoclass.findAll('h3')
            for link in links:
                url = link.find('a')['href']
                self.resolve_media(url,videos)
        except:
            pass

        try:
            links = videoclass.findAll('embed')
            for link in links:
                url = link.get('src')
                self.resolve_media(url,videos)
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
