'''
movierulz deccandelight plugin
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

class mrulz(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'https://movierulz.pl/category/'
        self.icon = self.ipath + 'mrulz.png'
        self.list = {'01Tamil Movies': self.bu + 'tamil-movie/',
                     '02Telugu Movies': self.bu + 'telugu-movie/',
                     '03Malayalam Movies': self.bu + 'malayalam-movie/',
                     '04Kannada Movies': self.bu + 'kannada-movie/',
                     '05Hindi 2018 Movies': self.bu + 'bollywood-movie-2018/',
                     '06Hindi 2017 Movies': self.bu + 'bollywood-movie-2017/',
                     '07Hindi 2016 Movies': self.bu + 'bollywood-movie-2016/',
                     '08English 2018 Movies': self.bu + 'hollywood-movie-2018/',
                     '09English 2017 Movies': self.bu + 'hollywood-movie-2017/',
                     '10English 2016 Movies': self.bu + 'hollywood-movie-2016/',
                     '11Tamil Dubbed Movies': self.bu + 'tamil-dubbed-movie-2/',
                     '12Telugu Dubbed Movies': self.bu + 'telugu-dubbed-movie-2/',
                     '13Hindi Dubbed Movies': self.bu + 'hindi-dubbed-movie/',
                     '14Bengali Movies': self.bu + 'bengali-movie/',
                     '15Punjabi Movies': self.bu + 'punjabi-movie-2016/',
                     '16[COLOR cyan]Adult Movies[/COLOR]': self.bu + 'adult-movie/',
                     '17[COLOR cyan]Adult 18+[/COLOR]': self.bu + 'adult-18/',
                     '99[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}
                    
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Movie Rulz')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'id':'container'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('nav', {'id':'posts-nav'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'class':'boxed film'})
        
        for item in items:
            title = h.unescape(item.text)
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
        
        if 'Older' in str(Paginator):
            nextli = Paginator.find('div', {'class':'nav-older'})
            purl = nextli.find('a')['href']
            pages = purl.split('/')
            currpg = int(pages[len(pages)-2]) - 1
            title = 'Next Page.. (Currently in Page %s)' % (currpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'entry-content'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('a')
            for link in links:
                vidurl = link.get('href')
                self.resolve_media(vidurl,videos)
        except:
            pass
            
        return videos
