'''
mersalaayitten deccandelight plugin
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

class mersal(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://mersalaayitten.live/videos?c='
        self.icon = self.ipath + 'mersal.png'
        self.hdstr = self.settings('mersalhd')
        self.list = {'01Tamil Movies': self.bu + '1&o=mr',
                     '02Telugu Movies': self.bu + '3&o=mr',
                     '03Hindi Movies': self.bu + '2&o=mr',
                     '04Malayalam Movies': self.bu + '4&o=mr',
                     '05Dubbed Movies': self.bu + '6&o=mr',
                     '06Animation Movies': self.bu + '5&o=mr',
                     '07[COLOR yellow]** Search **[/COLOR]': self.bu[:-9] + 'search?search_type=videos&search_query='}
   
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        movies = []
        h = HTMLParser.HTMLParser()
        if '%' in url:
            url = urllib.unquote(url)
        if url[-6:] == 'query=':
            search_text = self.get_SearchQuery('Mersalaayitten')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        headers = self.hdr
        headers['Accept-Encoding'] = 'deflate'
        html = requests.get(url, headers=headers).text
        mlink = SoupStrainer('div', {'class':'col-md-9 col-sm-8'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        plink = SoupStrainer("ul", {"class":"pagination pagination-lg"})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        items = mdiv.findAll('div', {'class':'col-sm-6 col-md-4 col-lg-4'})
        for item in items:
            title = h.unescape(item.find('span').text).encode('utf8')
            url = item.find('a')['href']
            url = self.bu[:-9] + 'media/nuevo/econfig.php?key=%s-0-0'%url.split('/')[-2]
            try:
                thumb = item.find('img')['data-original']
            except:
                thumb = item.find('img')['src']
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextpg = Paginator.find('a', {'class':'prevnext'})
            purl = nextpg.get('href')
            purl = urllib.quote_plus(purl)
            currpg = Paginator.find('li', {'class':'active'}).text
            pages = Paginator.findAll('li', {'class':'hidden-xs'})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,9)
      
    def get_video(self,url):

        rurl = self.bu[:-9]
        headers = self.hdr
        headers['Accept-Encoding'] = 'deflate'
        headers['Referer'] = rurl
        link = requests.get(url, headers=headers).text
            
        stream_url = re.findall('<file>([^<]+)',link)[0]
        if self.hdstr == 'true':
            try:
                stream_url = re.findall('<filehd>([^<]+)',link)[0]
            except:
                pass
        
        if '.mp4' not in stream_url:
            slink = requests.get(stream_url, headers=headers, allow_redirects=False)
            stream_url = slink.headers.get('location')

        try:
            srtfile = re.findall('<captions>([^<]+)',link)[0]
        except:
            srtfile = None

        r = requests.head(stream_url,headers=headers)
        if r.status_code >399:
            stream_url = stream_url.replace('/MA/','/')

        stream_url += '|User-Agent=%s'%self.hdr['User-Agent']
        return (stream_url,srtfile)