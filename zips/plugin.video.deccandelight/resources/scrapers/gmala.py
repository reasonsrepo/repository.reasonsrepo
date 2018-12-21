'''
Hindi Geetmala deccandelight plugin
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

class gmala(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.hindigeetmala.net'
        self.icon = self.ipath + 'gmala.png'
        self.list = {'02Browse by Movie Titles': self.bu + '/ZZZZTitles',
                     '03Browse Yearwise': self.bu + '/ZZZZYearwise',
                     '04Browse by Singer': self.bu + '/ZZZZSinger',
                     '05[COLOR yellow]** Search by Singer **[/COLOR]': self.bu + '/search.php?type=1&value=MMMM7',
                     '06[COLOR yellow]** Search by Composer **[/COLOR]': self.bu + '/search.php?type=2&value=MMMM7',
                     '07[COLOR yellow]** Search by Movie **[/COLOR]': self.bu + '/search.php?type=3&value=MMMM7',
                     '08[COLOR yellow]** Search by Song **[/COLOR]': self.bu + '/search.php?type=8&value=MMMM7'}
                     
    def get_menu(self):
        return (self.list,4,self.icon)

    def get_top(self,iurl):
        """
        Get the list of Categories.
        :return: list
        """
        categories = []
        url = iurl.split('ZZZZ')[0]
        category = iurl.split('ZZZZ')[1]
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('td', {'class':re.compile('^h20')})
        items = BeautifulSoup(html, parseOnlyThese=mlink)
        for item in items:
            if category in item.span.text:
                letters = item.findAll('a')
                for letter in letters:
                    title = letter.text
                    url = self.bu + letter.get('href')
                    icon = self.icon
                    categories.append((title,icon,url))        
        
        return (categories,5)
        
    def get_second(self,iurl):
        """
        Get the list of categories.
        :return: list
        """
        categories = []
        html = requests.get(iurl, headers=self.hdr).text
        
        mlink = SoupStrainer('table', {'class':'b1 w760 alcen'})
        itemclass = BeautifulSoup(html, parseOnlyThese=mlink)
        items = itemclass.findAll('td', {'class':'w25p h150'})
        for item in items:
            title = item.text
            url = self.bu + item.a.get('href')
            try:
                icon = self.bu + item.img.get('src')
            except:
                icon = self.icon
            categories.append((title,icon,url))

        plink = SoupStrainer('td', {'class':'vatop w140'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        pages = Paginator.findAll('td')
        for page in pages:
            if 'next' in str(page):
                ppath = page.find('a')['href']
                if ppath[0] == '/':
                    purl = self.bu + ppath
                else:
                    ptop = re.findall('(.+/)',iurl)[0]
                    purl = '%s%s'%(ptop,ppath)
                pgtxt = re.findall('(Page.*?)"',html)[0]
                if pgtxt.split()[1] != pgtxt.split()[3]:
                    title = 'Next Page.. (Currently in %s)' % pgtxt
                    categories.append((title,self.nicon,purl))
    
        return (categories,7)
        
    def get_items(self,iurl):
        h = HTMLParser.HTMLParser()
        movies = []
        if iurl[-7:] == '&value=':
            search_text = self.get_SearchQuery('Hindi Geetmala')
            search_text = urllib.quote_plus(search_text)
            iurl = iurl + search_text
        nextpg = True
        while len(movies)<50 and nextpg:
            html = requests.get(iurl, headers=self.hdr).text
            mlink = SoupStrainer('table', {'class':re.compile('allef$')})
            mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
            items = mdiv.findAll('tr')
            for item in items:
                albumdiv = item.find('td', {'itemprop':'inAlbum'})
                try:
                    title = albumdiv.text + '-> '
                except:
                    title = ''
                titlediv = item.find('td', {'class':'w185'})
                title += titlediv.find('span').text
                url = self.bu + titlediv.find('a')['href']
                icon = self.icon
                movies.append((title,icon,url))

            plink = SoupStrainer('td', {'class':'vamid w140'})
            Paginator = BeautifulSoup(html, parseOnlyThese=plink)
            if 'next' in str(Paginator):
                ppath = Paginator.find('a')['href']
                if ppath[0] == '/':
                    iurl = self.bu + ppath
                else:
                    ptop = re.findall('(.+/)',iurl)[0]
                    iurl = '%s%s'%(ptop,ppath)                
            else:
                nextpg = False

        if nextpg:
            pgtxt = re.findall('(Page.*?)"',html)[0]
            if pgtxt.split()[1] != pgtxt.split()[3]:
                title = 'Next Page.. (Currently in %s)' % pgtxt
                movies.append((title,self.nicon,iurl))
        
        return (movies,9)

    def get_video(self,url):
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('table', {'class':'b1 w760 alcen'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            link = videoclass.find('iframe')
            vidurl = link.get('src')
        except:
            vidurl = ''
            
        return vidurl
