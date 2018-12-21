'''
tamiltvshows deccandelight plugin
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
from resources.lib import unwise
import urllib, re, requests
import HTMLParser
#import xbmc

class ttvs(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.tamiltvshows.net/category/'
        self.icon = self.ipath + 'ttvs.png'
        self.list = {'01Recently Added': self.bu[:-9],
                     '02Sun TV Series': self.bu + 'tamil-serials/sun-tv-serials/',
                     '03Sun TV Shows': self.bu + 'tamil-tv-shows/sun-tv-shows/',
                     '04Vijay TV Series': self.bu + 'tamil-serials/vijay-tv-serials/',
                     '05Vijay TV Shows': self.bu + 'tamil-tv-shows/vijay-tv-shows/',
                     '06Zee Tamil TV Series': self.bu + 'tamil-serials/zee-tamil-serials/',
                     '07Zee Tamil TV Shows': self.bu + 'tamil-tv-shows/zee-tv-shows/',
                     '08Raj TV Series': self.bu + 'tamil-serials/raj-tv-serials/',
                     '09Raj TV Shows': self.bu + 'tamil-tv-shows/raj-tv-shows/',
                     '10Jaya TV Series': self.bu + 'tamil-serials/jaya-tv-serials/',
                     '11Jaya TV Shows': self.bu + 'tamil-tv-shows/jaya-tv-programs/',
                     '13Kalaignar TV Shows': self.bu + 'tamil-tv-shows/kalaignar-tv-shows/',
                     '30Polimer TV Serials': self.bu + 'tamil-serials/polimer-tv-serials/',
                     '31Captain TV Shows': self.bu + 'tamil-tv-shows/captain-tv-shows/',
                     '32Puthuyugam TV Shows': self.bu + 'tamil-tv-shows/puthuyugam/',
                     '33Puthiya Thalaimurai TV Shows': self.bu + 'tamil-tv-shows/puthiya-thalaimurai-tv-shows/',
                     '99[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + '?s='}

    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Tamil TV Shows')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('article')
        items = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer('div', {'class':re.compile('^post-pagination')})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        
        for item in items:
            title = h.unescape(item.h4.a.text)
            title = self.clean_title(title)
            url = item.find('a')['href']
            try:
                thumb = item.find('img')['src']
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextli = Paginator.find('a', {'class':re.compile('^next')})
            purl = nextli.get('href')
            currpg = Paginator.find('span', {'class':re.compile('current')}).text
            lastpg = Paginator.findAll('a', {'class':'page-numbers'})[-1].text
            title = 'Next Page.. (Currently in Page %s of %s)'%(currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
            
        html = requests.get(url, headers=self.hdr).text

        try:
            links = re.findall('(<iframe.+?iframe>)',html)
            for link in links:
                vidurl = re.findall('src="([^"]+)',link)[0]
                #xbmc.log("vid_url = %s" %vidurl,xbmc.LOGNOTICE)
                if 'tamiltvtube' in vidurl:
                    headers = self.hdr
                    headers['Referer'] = url
                    slink = requests.get(vidurl, headers=headers).text
                    hoster = 'TamilTVTube '
                    srclist = re.findall('(\[.*?\])', slink)[0]
                    strlinks = eval(srclist)
                    for strlink in strlinks:
                        elink = strlink['file']
                        if '&' in elink:
                            elink = urllib.quote(elink)
                        try:
                            qual = strlink['label']
                        except:
                            qual = 'HLS'
                        vidhost = hoster + qual
                        videos.append((vidhost,elink))
                
                elif 'videozupload' in vidurl:
                    headers = self.hdr
                    headers['Referer'] = url
                    html = requests.get(vidurl, headers=headers).text
                    match = re.search('id="container"(.+?</script>)', html, re.DOTALL)
                    if match:
                        data = match.group(1)
                        while 'w,i,s,e' in data:
                            data = unwise.unwise_process(data)
                        match = re.search("source:\s*'([^']+)", data)
                        if match:
                            elink = match.group(1)
                            vidhost = 'GVideo'
                            videos.append((vidhost,elink))
                    
                else:
                    vidurl = vidurl.split('&')[0]
                    self.resolve_media(vidurl,videos)
        except:
            pass

        try:
            vidurl = re.findall("window.open\('([^']+)",html)[0]
            vidurl = vidurl.split('&')[0]
            if 'tv?vq=medium#/' in vidurl:
                vidurl = vidurl.replace('tv?vq=medium#/','')
            self.resolve_media(vidurl,videos)
        except:
            pass
            
        return videos
