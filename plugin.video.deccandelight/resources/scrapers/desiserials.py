'''
yodesi deccandelight plugin
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
import xbmcgui

class badtameezdil(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.desi-serials.org/'
        self.icon = self.ipath + 'yodesi.png'
        self.list = {'02Star Plus': self.bu + 'star-plus-hdepisodes//',
                     '03Colors': self.bu + 'color-tv-hd/',
                     '04Zee TV': self.bu + 'zee-tv/',
                     '05Sony TV': self.bu + 'sony-tv/',
                     '06SAB TV': self.bu + 'sab-tv/',
                     '09& TV': self.bu + 'and-tv/'}
                     
    def get_menu(self):
        return (self.list,5,self.icon)

    def get_second(self,iurl):
        """
        Get the list of shows.
        :return: list
        """
        shows = []
        h = HTMLParser.HTMLParser()
        html = requests.get(iurl, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'slidewrap'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('div', {'class':re.compile('^four columns item')})
        for item in items:
            title = h.unescape(item.h4.text)
            url = item.find('a')['href']
            try:
                icon = "http://www.desi-serials.org" + item.find('img')['src']
            except:
                icon = self.icon
            
            shows.append((title,icon,url))
        
        return (shows,7)
        
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Yo Desi!')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'eleven columns top bottom'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('nav', {'role':'navigation'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('h2', {'class':'title bottom-2 top-2'})
        
        for item in items:
            title = h.unescape(item.a.text)
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextli = Paginator.find('a', {'class':'next page-numbers'})
            purl = nextli.get('href')
            currpg = Paginator.find('span', {'class': re.compile('current')}).text
            pages = Paginator.findAll('a', {'class':'page-numbers'})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
        h = HTMLParser.HTMLParser()    
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':re.compile('post-content bottom')})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            vidlinks = videoclass.findAll('a')
            for lik in vidlinks:
                vidurll = lik.get('href')
                html = requests.get(vidurll, headers=self.hdr).text
                getlink = re.findall("<iframe.+?src='(.+?)' frameborder='0' allowfullscreen><\/iframe><br>",html)[0]
                self.resolve_media(getlink,videos)
        except:
            pass

        try:
            pDialog = xbmcgui.DialogProgress()
            pDialog.create('Deccan Delight', 'Collecting Links...')
            prog_per = 0
            numlink = 0
            links = videoclass.findAll('a')
            for link in links:
                vidurl = link.get('href')
                vidtxt = h.unescape(link.text)
                vidtxt = re.findall('(\d.*)',vidtxt)[0]
                self.resolve_media(vidurl,videos,vidtxt)
                prog_per += 100/len(links)
                numlink += 1
                if (pDialog.iscanceled()): return videos
                pDialog.update(prog_per, 'Collected Links... %s of %s'%(numlink,len(links)))
        except:
            pass
            
        return videos
