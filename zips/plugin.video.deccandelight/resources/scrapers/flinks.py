'''
filmlinks4u deccandelight plugin
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

class flinks(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'https://www.filmlinks4u.is/category/'
        self.icon = self.ipath + 'flinks.png'
        self.list = {'01Tamil Movies': self.bu + 'tamil',
                     '02Telugu Movies': self.bu + 'telugu',
                     '03Malayalam Movies': self.bu + 'malayalam',
                     '04Kannada Movies': self.bu + 'kannada',
                     '05Hindi Movies': self.bu + 'hindi',
                     '06English Movies': self.bu + 'hollywood',
                     '07Animation Movies': self.bu + 'animation',
                     '08Biography Movies': self.bu + 'biography',
                     '09Documentary Movies': self.bu + 'documentary',
                     '10Bengali Movies': self.bu + 'bengali',
                     '11Bhojpuri Movies': self.bu + 'bhojpuri',
                     '12Gujarati Movies': self.bu + 'gujarati',
                     '13Marathi Movies': self.bu + 'marathi',
                     '14Oriya Movies': self.bu + 'oriya',
                     '15Punjabi Movies': self.bu + 'punjabi',
                     '16Rajasthani Movies': self.bu + 'rajasthani',
                     '17Urdu Movies': self.bu + 'urdu',
                     '18Nepali Movies': self.bu + 'nepali',
                     '97[COLOR cyan]Hindi Adult Softcore[/COLOR]': self.bu + 'adult-hindi-short-films',
                     '98[COLOR cyan]Adult Movies[/COLOR]': self.bu + 'adult',
                     '99[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}
                     
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Film Links 4U')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        #mlink = SoupStrainer('div', {'class':re.compile('content')})
        #mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':'pagination'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = re.findall('<article.*?a href="(.*?)">(.*?)<.*?post-cats">(.*?)</span.*?<img.*?src="(.*?)"',html,re.DOTALL)
        
        for item in items:
            title = h.unescape(item[1])
            title = self.clean_title(title)
            url = item[0]
            try:
                thumb = item[3]
            except:
                thumb = self.icon
            if 'adult' not in item[2].lower():
                movies.append((title, thumb, url))
            elif self.adult == 'true':
                movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextli = Paginator.find('span', {'id':'tie-next-page'})
            purl = nextli.find('a')['href']
            pgtxt = Paginator.find('span', {'class':'pages'}).text
            title = 'Next Page.. (Currently in %s)' % pgtxt
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'content'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            tabsdiv = videoclass.find('div', {'class':'tabs'})
            tabs = tabsdiv.findAll('div', {'class':re.compile('^tab embed')})
            for tab in tabs:
                vidurl = tab.get('data-href')
                self.resolve_media(vidurl,videos)
        except:
            pass

        try:
            linksdiv = videoclass.find('div', {'class':'entry'})
            plinks = linksdiv.findAll('p')
            for plink in plinks:
                r = re.search('target="_blank"[^>]+class="external"',str(plink))
                if r:
                    alinks = plink.findAll('a')
                    for alink in alinks:
                        vidurl = alink.get('href')
                        vidtxt = ''
                        t = re.search('(Part\s*\d*)',alink.text)
                        if t:
                            vidtxt = t.group(1)
                        self.resolve_media(vidurl,videos,vidtxt)
        except:
            pass
            
        return videos
