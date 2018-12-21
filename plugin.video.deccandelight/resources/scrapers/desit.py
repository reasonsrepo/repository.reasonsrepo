'''
desitashan deccandelight plugin
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

class desit(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.desitashan.tv/'
        self.icon = self.ipath + 'desit.png'
            
    def get_menu(self):
        html = requests.get(self.bu, headers=self.hdr).text
        mlink = SoupStrainer('ul', {'class':'td-mobile-main-menu'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('li')
        self.list = {}
        ino = 1
        for item in items:
            self.list['%02d%s'%(ino,item.text)]=item.find('a')['href']
            ino+=1
        self.list['99[COLOR yellow]** Search **[/COLOR]']= self.bu + '?s=MMMM7'
        return (self.list,5,self.icon)

    def get_second(self,iurl):
        """
        Get the list of shows.
        :return: list
        """
        shows = []
        h = HTMLParser.HTMLParser()

        html = requests.get(iurl, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':re.compile('td-page-content')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('li')
        thumb = mdiv.find('img')['src']
        for item in items:
            title = h.unescape(item.text)
            url = item.find('a')['href']
            shows.append((title,thumb,url))

        return (shows,7)
        
    def get_items(self,iurl):
        episodes = []
        h = HTMLParser.HTMLParser()
        if iurl[-3:] == '?s=':
            search_text = self.get_SearchQuery('Desi Tashan')
            search_text = urllib.quote_plus(search_text)
            iurl += search_text
        nextpg = True
        while nextpg and len(episodes)<21:
            html = requests.get(iurl).text
            mlink = SoupStrainer('div', {'class':'td-ss-main-content'})
            mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
            items = mdiv.findAll('div', {'class':'td-block-span6'})
            for item in items:
                title = h.unescape(item.h3.text)
                if 'video' in title.lower():
                    title = self.clean_title(title)
                    url = item.find('a')['href']
                    try:
                        icon = item.find('img')['src']
                    except:
                        icon = self.icon           
                    episodes.append((title,icon,url))
                    
            plink = SoupStrainer('div', {'class':re.compile('^page-nav')})
            Paginator = BeautifulSoup(html, parseOnlyThese=plink)

            if 'menu-right' in str(Paginator):
                currpg = Paginator.find('span', {'class':'current'}).text
                nlinks = Paginator.findAll('a', {'class':None})
                for nlink in nlinks:
                    if 'menu-right' in str(nlink):
                        iurl = nlink.get('href')
                if len(episodes)>20:
                    pgtxt = Paginator.find('span', {'class':'pages'}).text
                    title = 'Next Page.. (Currently in %s)' % pgtxt
                    episodes.append((title, self.nicon, iurl))
            else:
                nextpg = False
        return (episodes,8) 

    def get_videos(self,iurl):
        videos = []
        h = HTMLParser.HTMLParser()
        html = requests.get(iurl).text
        mlink = SoupStrainer('div', {'class':re.compile('^td-post-content')})
        videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
        items = videoclass.findAll('a', {'class':None})
        if len(items) < 1:
            items = videoclass.findAll('a', {'class':re.compile('nofollow')})
        prog_per = 0
        numlink = 0
        pDialog = xbmcgui.DialogProgress()
        pDialog.create('Deccan Delight', 'Collecting Links...')
        for item in items:
            vid_link = item['href']
            vidtxt = h.unescape(item.text)
            try:
                vidtxt = re.findall('(Part\s*\d*)',vidtxt)[0]
            except:
                vidtxt = ''
            self.resolve_media(vid_link,videos,vidtxt)
            prog_per += 100/len(items)
            numlink += 1
            if (pDialog.iscanceled()): return videos
            pDialog.update(prog_per, 'Collected Links... %s of %s'%(numlink,len(items)))
        return videos
