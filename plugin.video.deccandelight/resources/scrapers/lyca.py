'''
lycamusic deccandelight plugin
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
import re, requests

class lyca(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://athavantv.com/live/'
        self.icon = self.ipath + 'lyca.png'
        self.list = {'01Athavan TV': self.bu + 'live-auto-athavan.php',
                     '02Athavan Music HD': self.bu + 'live-auto-musichd.php',
                     '03Athavan Classic': self.bu + 'live-auto-clasic.php'}
                  
    def get_menu(self):
        return (self.list,9,self.icon)
    
    def get_video(self,url):
        html = requests.get(url, headers=self.hdr).text
        strurl = re.findall('file:\s*"([^"]+)',html)[0]
        if strurl.startswith('//'):
            strurl = 'http:' + strurl
        return strurl