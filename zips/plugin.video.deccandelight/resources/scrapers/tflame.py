'''
telugu-flame deccandelight plugin
Copyright (C) 2018 Gujal

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
import re, requests, json, urllib, HTMLParser


class tflame(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'https://www.teluguflame.net/'
        self.icon = self.ipath + 'tflame.png'
        self.list = {'01ETV Serials': 'ETV Serials',
                     '02ETV Shows': 'ETV Shows',
                     '03Gemini TV Serials':  'Geminitv Serials',
                     '04Gemini TV Shows': 'GeminiTV & MISC Shows',
                     '05MAA TV Serials': 'MAA Serials',
                     '06MAA TV Shows': 'MAA TV & ETVPLUS Shows',
                     '07Zee Telugu Serials': 'Zee Telugu Serials',
                     '08Zee Telugu Shows': 'Zee Telugu Shows'}
           
    def get_menu(self):
        return (self.list,5,self.icon)

    def get_second(self,iurl):
        """
        Get the list of shows.
        :return: list
        """
        html = requests.get(self.bu, headers=self.hdr).content
        mlink = SoupStrainer('ul', {'class':'mega-nav'})
        items = BeautifulSoup(html, parseOnlyThese=mlink)
        menu = {}
        for item in items:
            for eachitem in item.findAll('ul'):
                cat = eachitem.findParent('li').a.text
                cat_items = []
                for li in eachitem.findAll('li'):
                    title = li.text
                    url = li.find('a')['href']
                    if not(url.endswith('/')):
                        url += '/'
                    cat_items.append((title,url))
                menu[cat]=cat_items

        categories = []
        for title,url in menu[iurl]:
            categories.append((title,self.icon,url))   
        
        return (categories,7)
        
    def get_items(self,url):
        movies = []
        h = HTMLParser.HTMLParser()
        html = requests.get(url, headers=self.hdr).content
        mlink = SoupStrainer('div', {'class':'post-content'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('h3')
        try:
            thumb = mdiv.find('img')['src']
        except:
            thumb = self.icon
        for item in items:
            if 'ClickHere' in item.text:
                title = h.unescape(item.text).replace('ClickHere','').replace(':',' ').encode('utf8')
                url = item.a.get('href')
                movies.append((title, thumb, url))
        
        # if 'next page' in mdiv.lower():
            # purl = re.findall('href="([^"]+)"\s*>\s*Next',mdiv)[0]
            # movies.append(('Next Page..', self.nicon, purl))
        
        return (movies,9)

    def un(self,sid):
        j = 0
        s2 = ''
        while j < len(sid):
            s2 += '\\u0' + sid[j:(j + 3)]
            j += 3
        jd = json.loads(s2.decode('unicode-escape')) 
        return jd['v']
    
    def get_video(self,url):
        html = requests.get(url, headers=self.hdr).content
        mlink = SoupStrainer('div', {'class':'post-content'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)        
        stream_url = False
        if 'hqq.' in str(mdiv) or '<script' in str(mdiv) :
            if 'hash.php?hash' in str(mdiv):
                ids = mdiv.findAll('script')
                eurl = ids[0].get('src')
                ehtml = requests.get(eurl, headers=self.hdr).content
                ecode = urllib.unquote(re.findall('"([^"]+)',ehtml)[0])
                vals = re.findall('=\s*(\{[^;]+)',ecode)[0]
                vid = re.findall("vid':'([^']+)",vals)[0]
                hsh = re.findall("from':'([^']+)",vals)[0]
                stream_url = 'https://hqq.watch/player/embed_player.php?vid=%s&autoplay=none&hash_from=%s'%(vid,hsh)
            else:
                ids = mdiv.findAll('div', {'id':True})
                sid = ids[0].get('id')
                vid_f = self.un(sid)
                stream_url = 'https://hqq.watch/player/embed_player.php?vid=%s&autoplay=none'%vid_f
        else:
            try:
                stream_url = mdiv.find('iframe')['src']
            except:
                stream_url = mdiv.find('a')['href']

        return stream_url