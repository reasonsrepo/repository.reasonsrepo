'''
ozee deccandelight plugin
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
import re, requests
import HTMLParser
import resources.lib.jscrypto as jscrypto

class ozee(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://www.ozee.com/'
        self.icon = self.ipath + 'ozee.png'
        self.list = {'01Shows': self.bu + 'shows/all',
                     '02Movies': self.bu + 'movies/all',
                     '03Videos': self.bu + 'videos/all',
                     '04Music': self.bu + 'music/all'}
            
    def get_menu(self):
        return (self.list,4,self.icon)

    def get_top(self,url):
        """
        Get the list of channels.
        :return: list
        """
        channels = []
        h = HTMLParser.HTMLParser()
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':'filter-container'})
        fdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        if 'videos' in url or 'music' in url:
            mdiv=fdiv.find('select', {'id':'genre_select'})
            items = mdiv.findAll('option', {'data-type':'genre'})
        elif 'shows' in url:
            mdiv=fdiv.find('select', {'id':'channel_select'})
            items = mdiv.findAll('option', {'data-type':'lang'})
        else:
            mdiv=fdiv.find('select', {'id':'lang_select'})
            items = mdiv.findAll('option', {'data-type':'lang'})
        for item in items:
            title = h.unescape(item.text)
            iurl = '%s/%s'%(url,item['value'])
            channels.append((title,self.icon,iurl))

        return (channels,5)

    def get_second(self,url):
        """
        Get the list of shows.
        :return: list
        """
        shows = []
        h = HTMLParser.HTMLParser()
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':re.compile('^col-md-2')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('div', {'class':re.compile('^thumbnail')})
        for item in items:
            title = h.unescape(item.span.text)
            if '/shows/' in url:
                iurl = item.find('a')['href'] + '/video'
            else:
                iurl = item.find('a')['href']
            icon = item.find('img')['src']
            shows.append((title,icon,iurl))
            
        plink = SoupStrainer('ul', {'class':'pagination'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        if 'next' in str(Paginator):
            nlink = Paginator.find('a', {'rel':'next'})
            iurl = nlink.get('href')
            currpg = Paginator.find('li', {'class':'active'}).text
            pages = Paginator.findAll('a', {'rel':None})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            shows.append((title, self.nicon, iurl))
        
        if '/shows/' in url:
            nmode = 7
        else:
            nmode = 9
        
        return (shows,nmode)
        
    def get_items(self,url):
        episodes = []
        h = HTMLParser.HTMLParser()
        html = requests.get(url, headers=self.hdr).text
        mlink = SoupStrainer('div', {'class':re.compile('^col-md-3')})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('div', {'class':re.compile('^thumbnail')})
        for item in items:
            title = h.unescape(item.find('a')['title'])
            iurl = item.find('a')['href']
            icon = item.find('img')['src']
            episodes.append((title,icon,iurl))
            
        plink = SoupStrainer('ul', {'class':'pagination'})
        Paginator = BeautifulSoup(html, parseOnlyThese=plink)
        if 'next' in str(Paginator):
            nlink = Paginator.find('a', {'rel':'next'})
            url = nlink.get('href')
            currpg = Paginator.find('li', {'class':'active'}).text
            pages = Paginator.findAll('a', {'rel':None})
            lastpg = pages[len(pages)-1].text
            title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
            episodes.append((title, self.nicon, url))    
        
        return (episodes,9) 

    def get_video(self,url):
        html = requests.get(url, headers=self.hdr).text
        
        try:
            ct = re.findall('hlsplayurl = .{"ct":"(.*?)"',html)[0]
            salt = re.findall('hlsplayurl = .{.*?"s":"(.*?)"',html)[0]
            passphrase = re.findall('var dailytoday = "(.*?)"',html)[0]
            salt = salt.decode('hex')
            val = eval(jscrypto.decode(ct,passphrase,salt))
            stream_url = val.replace('\\','')
            if 'webisode' in stream_url:
                strurl,token = stream_url.split('?')
                strurl = strurl.replace('/Webisode','')
                url2 = strurl.split('Webisode')[0]
                epno = re.findall('episode-(.*?)-',url)[0]
                stream_url = '%sEpisode_%s.smil/master.m3u8?%s'%(url2,epno,token)
        except:
            stream_url = None
            
        return stream_url
