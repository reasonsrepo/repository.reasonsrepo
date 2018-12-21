'''
olangal deccandelight plugin
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

class olangal(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'https://olangal.se/'
        self.icon = self.ipath + 'olangal.png'
        self.list = {'01Recent Movies': self.bu,
                     '02[COLOR yellow]** Search **[/COLOR]': self.bu + '?s='}

    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Olangal')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':re.compile('^item_1')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        pdiv = mdiv.find('div', {'class':'paginado'})
        Paginator = mdiv.find('div', {'class':'pag_b'})
        items = mdiv.findAll('div', {'class':'item'})
        
        for item in items:
            title = h.unescape(item.h2.text)
            title = self.clean_title(title)
            url = item.find('a')['href']
            thumb = item.find('img')['src'].encode('utf8')
            movies.append((title, thumb, url))
        
        if 'Next' in Paginator.text:
            purl = Paginator.a.get('href')
            currpg = pdiv.find('a', {'class':'current'}).text
            pages = pdiv.findAll('li')
            lastpg = pages[len(pages)-1].find('a')['href'].split('page/')[1]
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'entry-content'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            pDialog = xbmcgui.DialogProgress()
            pDialog.create('Deccan Delight', 'Collecting Links...')
            prog_per = 0
            numlink = 0
            links = videoclass.findAll('a', {'rel':re.compile('noopener')})
            for link in links:
                vidurl = link.get('href')
                if 'olangal.' in vidurl:
                    html = requests.get(vidurl, headers=self.hdr).text
                    mlink = SoupStrainer('div', {'class':'entry-content'})
                    frameclass = BeautifulSoup(html, parseOnlyThese=mlink)
                    strurl = frameclass.find('iframe')['src']
                    self.resolve_media(strurl,videos)
                else:
                    self.resolve_media(vidurl,videos)
                prog_per += 100/len(links)
                numlink += 1
                if (pDialog.iscanceled()): return videos
                pDialog.update(prog_per, 'Collected Links... %s of %s'%(numlink,len(links)))
        except:
            pass

        try:
            links = videoclass.findAll('iframe')
            for link in links:
                vidurl = link.get('src')
                self.resolve_media(vidurl,videos)
        except:
            pass
      
        return videos
