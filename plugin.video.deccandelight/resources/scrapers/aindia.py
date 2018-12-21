'''
abroadindia deccandelight plugin
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
import requests, json, urllib


class aindia(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://abroadindia.com/k_loadlist.php?lan='
        self.icon = self.ipath + 'aindia.png'
        self.list = {'01Tamil Channels': self.bu + 'tamil',
                     '02Telugu Channels': self.bu + 'telugu',
                     '03Malayalam Channels': self.bu + 'malayalam',
                     '04Kannada Channels': self.bu + 'kannada',
                     '05Hindi Channels': self.bu + 'hindi',
                     '06English Channels': self.bu + 'english',
                     '07Sports Channels': self.bu + 'sports',
                     '08News Channels': self.bu + 'news',
                     '09Informative Channels': self.bu + 'informative',
                     '10Spiritual Channels': self.bu + 'spiritual',
                     '12[COLOR yellow]** Search **[/COLOR]': self.bu[:-4] + 's='}
  
    def get_menu(self):
        return (self.list,7,self.icon)
    
    def get_items(self,url):
        movies = []
        if url[-3:] == '?s=':
            search_text = self.get_SearchQuery('Abroad India')
            search_text = urllib.quote_plus(search_text)
            url = url + search_text

        html = requests.get(url, headers=self.hdr).text
        jdata = json.loads(html)
        for item in jdata[jdata.keys()[0]]:
            url = 'http://abroadindia.com/k_loadlink.php?cid=%s'%item['channel_id']
            title = item['channel_name']
            thumb = item['image_url']
            movies.append((title, thumb, url))
        movies.sort()
        
        return (movies,9)
      
    def get_video(self,iurl):

        r = requests.get(iurl, headers=self.hdr)
        echo_url = 'http://abroadindia.com/k_echo_stream.php'
        stream_url = requests.get(echo_url, headers=self.hdr).text.strip()
        if '//' not in stream_url:
            stream_url = None

        return stream_url
