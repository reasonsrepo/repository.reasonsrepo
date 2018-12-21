'''
india4movie deccandelight plugin
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

class i4movie(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'https://www.india4movie.com/category/'
        self.icon = self.ipath + 'i4movie.png'
        self.list = {'01Tamil Movies': self.bu + 'tamil-movie-list-2016-online-download/',
                     '02Telugu Movies': self.bu + 'telugu-movies-online-free/',
                     '03Malayalam Movies': self.bu + 'malayalam-movie-list/',
                     '04Kannada Movies': self.bu + 'kannada-new-movies-online/',
                     '05Hindi Movies': self.bu + 'hindi-movie/',
                     '06English Movies': self.bu + 'hollywood-movie/',
                     '07South Indian Dubbed in Hindi': self.bu + 'south-indian-in-hindi/',
                     '08Hollywood Dubbed in Hindi': self.bu + 'hoolywood-in-hindi-dubbed/',
                     '09Punjabi Movies': self.bu + 'punjabi-movies-list/',
                     '10Marathi Movies': self.bu + 'marathi/',
                     '11Bengali Movies': self.bu + 'bengali-new/',
                     '12Urdu Movies': self.bu + 'pakistani-movies/',
                     '98[COLOR cyan]Adult Movies[/COLOR]': self.bu + 'adult-new-movie-xxx/',
                     '99[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}
 
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('India 4 Movie')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'id':'content'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'wp-pagenavi'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'class':re.compile('^post')})
        
        for i in range(1,len(items)):
            item = items[i]
            title = h.unescape(item.h4.find('a')['title'])
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
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
        mlink = SoupStrainer('div', {'class':re.compile('^entry')})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('a')
            for link in links:
                vidurl = link.get('href')
                if ('india4movie' in vidurl) or ('imdb.' in vidurl):
                    pass
                else:
                    self.resolve_media(vidurl,videos)

        except:
            pass
      
        return videos
