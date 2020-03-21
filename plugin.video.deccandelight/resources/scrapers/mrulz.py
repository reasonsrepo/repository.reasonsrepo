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
                     '02Malayalam Movies': self.bu + 'malayalam-movie/',
                     '03Kannada Movies': self.bu + 'kannada-movie/',
                     '04Telugu 2020 Movies': self.bu + 'telugu-movies-2020/',
                     '05Telugu 2019 Movies': self.bu + 'telugu-movies-2019/',
                     '06Telugu 2018 Movies': self.bu + 'telugu-movies-2018/',
                     '07Telugu 2017 Movies': self.bu + 'telugu-movies-2017/',
                     '08Telugu 2016 Movies': self.bu + 'telugu-movies-2016/',
                     '09Hindi 2020 Movies': self.bu + 'bollywood-movie-2020/',
                     '10Hindi 2019 Movies': self.bu + 'bollywood-movie-2019/',
                     '11Hindi 2018 Movies': self.bu + 'bollywood-movie-2018/',
                     '12Hindi 2017 Movies': self.bu + 'bollywood-movie-2017/',
                     '13Hindi 2016 Movies': self.bu + 'bollywood-movie-2016/',
                     '14English 2020 Movies': self.bu + 'hollywood-movie-2020/',
                     '15English 2019 Movies': self.bu + 'hollywood-movie-2019/',
                     '16English 2018 Movies': self.bu + 'hollywood-movie-2018/',
                     '17English 2017 Movies': self.bu + 'hollywood-movie-2017/',
                     '18English 2016 Movies': self.bu + 'hollywood-movie-2016/',
                     '19Tamil Dubbed Movies': self.bu + 'tamil-dubbed-movie-2/',
                     '20Telugu Dubbed Movies': self.bu + 'telugu-dubbed-movie-2/',
                     '21Hindi Dubbed Movies': self.bu + 'hindi-dubbed-movie/',
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
