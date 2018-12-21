'''
tamilgun deccandelight plugin
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
import urllib, re, requests, json, HTMLParser
from resources.lib import jsunpack

class tgun(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://tamilgun.watch'
        self.icon = self.ipath + 'tgun.png'
    
    def get_menu(self):
        h = HTMLParser.HTMLParser()
        r = requests.get(self.bu, headers=self.hdr)
        if r.url != self.bu:
            self.bu = r.url
        items = {}
        cats = re.findall('id="menu-item-(?!4|5404|6147).*?href="((?=.*categories).*?)">((?!User).*?)<',r.text)
        sno = 1
        for cat in cats:
            items['0%s'%sno+h.unescape(cat[1]).encode('utf8')] = cat[0]
            sno+=1
        items['99[COLOR yellow]** Search **[/COLOR]'] = self.bu + '/?s='
        return (items,7,self.icon)
    
    def get_items(self,url):
        h = HTMLParser.HTMLParser()
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Tamil Gun')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('article', {'class':re.compile('video')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)

        plink = SoupStrainer('ul', {'class':'page-numbers'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)

        for item in mdiv:
            title = h.unescape(item.h3.text).encode('utf8')
            url = item.h3.find('a')['href']
            try:
                thumb = item.find('img')['src'].strip()
            except:
                thumb = self.icon
            movies.append((title, thumb, url))
        
        if 'next' in str(Paginator):
            nextli = Paginator.find('a', {'class':re.compile('next')})
            purl = nextli.get('href')
            if 'http' not in purl:
                purl = self.bu[:-12] + purl
            currpg = Paginator.find('span', {'class':re.compile('current')}).text
            pages = Paginator.findAll('a', {'class':re.compile('^page')})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            movies.append((title, self.nicon, purl))
        
        return (movies,8)

    def get_videos(self,url):
        videos = []
        if 'cinebix.com' in url:
            self.resolve_media(url,videos)
            return videos
            
        html = requests.get(url, headers=self.hdr).text
            
        try:
            linkcode = jsunpack.unpack(html).replace('\\','')
            sources = json.loads(re.findall('sources:(.*?)\}\)',linkcode)[0])
            for source in sources:    
                url = source['file'] + '|Referer=http://%s/'%self.get_vidhost(source['file'])
                url = urllib.quote_plus(url)
                videos.append(('tamilgun | %s'%source['label'],url))
        except:
            pass

        try:
            sources = json.loads(re.findall('(?s)sources:\s*(.*?)\}\)',html)[0])
            #ua = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
            for source in sources:    
                url = source['file']
                if 'play.php' in url:
                    #url += '|Referer=http://%s/'%self.get_vidhost(url)
                    url = urllib.quote_plus(url)
                    videos.append(('tamilgun | %s'%source['label'],url))
                else:
                    url += '|User-Agent=%s'%self.hdr['User-Agent']
                    url = urllib.quote_plus(url)
                    videos.append(('tamilgun live',url))
        except:
            pass

        mlink = SoupStrainer('div', {'id':'videoframe'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('iframe')
            for link in links:
                url = link.get('src')
                if 'http' not in url:
                    url = 'http:' + url
                self.resolve_media(url,videos)
        except:
            pass

        mlink = SoupStrainer('div', {'class':'entry-excerpt'})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)

        try:
            links = videoclass.findAll('iframe')
            for link in links:
                if 'http' in str(link):
                    url = link.get('src')
                    self.resolve_media(url,videos)
        except:
            pass

        try:
            links = videoclass.findAll('p')
            for link in links:
                if 'http' in str(link):
                    url = link.a.get('href')
                    self.resolve_media(url,videos)
        except:
            pass
        
        try:
            sources = json.loads(re.findall('vdf-data-json">(.*?)<',html)[0])
            url = 'https://www.youtube.com/watch?v=%s'%sources['videos'][0]['youtubeID']
            self.resolve_media(url,videos)
        except:
            pass
            
        return videos
        
    def get_video(self,url):
        headers = self.hdr
        headers['Referer'] = 'http://%s/'%self.get_vidhost(url)
        url += '&stream=1'
        html = requests.get(url, headers=self.hdr, allow_redirects=False)
        strurl = html.headers.get('location')
        return strurl
