'''
nextv deccandelight plugin
Copyright (C) 2017 Gujal

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
import re, requests


class nextv(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://nextvnow.live/index.php?lan='
        self.bcu = 'http://nextvnow.live/index.php?cat='
        self.lurl = self.bu[:-5]
        self.cj = requests.get(self.lurl,headers=self.dhdr).cookies
        self.icon = self.ipath + 'nextv.png'
        self.list = {'01Tamil Channels': self.bu + '4',
                     '02Telugu Channels': self.bu + '5',
                     '03Malayalam Channels': self.bu + '3',
                     '04Kannada Channels': self.bu + '6',
                     '05Hindi Channels': self.bu + '2',
                     '06English Channels': self.bu + '1',
                     '07Urdu Channels': self.bu + '11',
                     '08Arabic Channels': self.bu + '14',
                     '09Punjabi Channels': self.bu + '19',
                     '11Sports Channels': self.bcu + '3',
                     '12News Channels': self.bcu + '2',
                     '13Informative Channels': self.bcu + '10',
                     '14Spiritual Channels': self.bcu + '5'}
  
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        movies = []
        html = requests.get(url, cookies=self.cj, headers=self.dhdr).text
        items = re.findall('class="content"[^"]+"([^"]+).+?title">([^<]+)',html,re.DOTALL)
        for path,title in items:
            url = self.bu[:-14] + path
            thumb = self.icon
            movies.append((title, thumb, url))
        movies.sort()
        
        return (movies,9)
      
    def get_video(self,iurl):
        headers = self.dhdr
        headers['X-Requested-With']='com.jio.jioplay.livetv'
        html = requests.get(iurl, cookies=self.cj, headers=headers).text
        url = re.findall('href="([^"]+)"\s*id="play',html)[0]
        strurl = self.bu[:-14] + url
        r = requests.get(strurl, cookies=self.cj, headers=headers, allow_redirects=False).headers
        stream_url = r['Location']
        if 'yupptvredirect' in stream_url or 'jio.com' in stream_url:
            r = requests.get(stream_url, cookies=self.cj, headers=headers, verify=False, allow_redirects=False).headers
            stream_url = r['Location'] 
            if 'jio.com' in stream_url:
                stream_url += '|User-Agent=%s'%self.jhdr['User-Agent']
            else:
                stream_url += '|User-Agent=%s'%self.dhdr['User-Agent']
        return stream_url
