'''
hindilinks4u deccandelight plugin
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
import urllib, re, requests, xbmc
import HTMLParser

class hlinks(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'https://www.hindilinks4u.to/category/'
        self.icon = self.ipath + 'hlinks.png'
        self.list = {'01Hindi Movies': self.bu + 'hindi-movies',
                     '02Dubbed Movies': self.bu + 'dubbed-movies',
                     '03Documentary Movies': self.bu + 'documentaries',
                     '04[COLOR cyan]Adult Movies[/COLOR]': self.bu + 'adult',
                     '05[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}
                  
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Hindi Links 4U')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'nag cf'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'wp-pagenavi'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'id':re.compile('^post-')})
        
        for item in items:
            title = h.unescape(item.find('a')['title'])
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            movdet = item.find('p', {'class':'entry-summary'}).text.lower()
            if 'adult' not in movdet and 'short' not in movdet:
                movies.append((title, thumb, url))
            elif self.adult == 'true':
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
        mlink = SoupStrainer('div', {'class':'entry-content rich-content'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            vtabs = re.findall('data-href=."(.*?)."',html)
            for vtab in vtabs:
                self.resolve_media(vtab,videos)
        except:
            pass

        try:
            links = videoclass.findAll('a')
            for link in links:
                vidurl = link.get('href')
                self.resolve_media(vidurl,videos)
        except:
            pass
            
        return videos
