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

class yodesi(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.yodesitv.co/'
        self.icon = self.ipath + 'yodesi.png'
        self.list = {'02Star Plus': self.bu + 'star-plus/',
                     '03Colors': self.bu + 'colors/',
                     '04Zee TV': self.bu + 'zee-tv/',
                     '05Sony TV': self.bu + 'sony-tv/',
                     '06SAB TV': self.bu + 'sab-tv/',
                     '07Life OK': self.bu + 'life-ok/',
                     '08Star Jalsha': self.bu + 'star-jalsha/',
                     '09& TV': self.bu + 'tv-and-tv/',
                     '10Star Pravah': self.bu + 'star-pravah/',
                     '11Star Vijay': self.bu + 'star-vijay/',
                     '11MTV': self.bu + 'mtv-india/',
                     '12Bindass': self.bu + 'bindass-tv/',
                     '13Channel V': self.bu + 'category/channel-v/MMMM7',
                     '14E 24': self.bu + 'category/e24/MMMM7',
                     '15Promos': self.bu + 'category/promos-section/MMMM7',
                     '16[COLOR yellow]** Search **[/COLOR]': self.bu + '?s=MMMM7'}
                     
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
        mlink = SoupStrainer('div', {'id':'content_box'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('div', {'class':re.compile('^one_')})
        for item in items:
            title = h.unescape(item.text)
            url = item.find('a')['href']
            try:
                icon = item.find('img')['src']
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
        mlink = SoupStrainer('div', {'class':'main-container'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('nav', {'role':'navigation'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'class':'latestPost-content'})
        
        for item in items:
            title = h.unescape(item.h2.text)
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
        mlink = SoupStrainer('div', {'class':re.compile('entry-content')})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('iframe')
            for link in links:
                vidurl = link.get('src')
                self.resolve_media(vidurl,videos)
        except:
            pass

        try:
            pDialog = xbmcgui.DialogProgress()
            pDialog.create('Deccan Delight', 'Collecting Links...')
            prog_per = 0
            numlink = 0
            links = videoclass.findAll('a', {'target':'_blank'})
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
