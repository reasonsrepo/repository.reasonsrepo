'''
thoptv deccandelight plugin
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
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib, re, requests, base64, random
import HTMLParser
import xbmc

class thop(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://thoptv.stream/channels/'
        self.icon = self.ipath + 'thop.png'
        self.qvalues = ['Low','Med','Default','Good','High']
        self.bvalues = ['250','400','600','800','1200']
        self.qual = self.qvalues[int(self.settings('thopqual'))]
        self.bitrate = self.bvalues[int(self.settings('thopqual'))]
        self.list = {'01Tamil TV': self.bu + 'tamil/',
                     '02Telugu TV': self.bu + 'telugu/',
                     '03Malayalam TV': self.bu + 'malayalam/',
                     '04Kannada TV': self.bu + 'kannada/',
                     '05Hindi TV': self.bu + 'hindi/',
                     '06English TV': self.bu + 'english/',
                     '08Marathi TV': self.bu + 'marathi/',
                     '10Gujarati TV': self.bu + 'gujarati/'}
            
    def get_menu(self):
        return (self.list,7,self.icon)
        
    def get_items(self,iurl):
        channels = []
        h = HTMLParser.HTMLParser()
        mlink = SoupStrainer('div', {'class':'items'})
        plink = SoupStrainer('div', {'class':'resppages'})
        nextpg = True
        while nextpg:
            nextpg = False
            html = requests.get(iurl, headers=self.hdr).text
            mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
            items = mdiv.findAll('article')
            for item in items:
                title = h.unescape(item.h3.text).encode('utf8')
                if '(' in title:
                    title = re.findall('(.+?)\s\(',title)[0]
                url = item.h3.find('a')['href']
                thumb = item.find('img')['src']
                channels.append((title, thumb, url))
            Paginator = BeautifulSoup(html, parseOnlyThese=plink)
            if 'chevron-right' in str(Paginator):
                iurl = Paginator.findAll('a')[-1].get('href')
                nextpg = True
        return (sorted(channels),9) 

    def get_video(self,url):

        html = requests.get(url, headers=self.hdr).text
        stream_url = ''
        b = base64.b64decode
        
        def concat(*args):
            base = []
            for item in args:
                base+=item
            return base[:]

        try:
            stream_url = re.findall("Clappr\.Player.+?source:\s*'([^']+)", html)[0]
        except:
            pass
        
        if stream_url == '':
            tlink = re.findall('<iframe.+?src=[\'"]([^\'"]+)', html)[0]
            if 'url=' in tlink:
                tlink = re.findall('url=(.*)',tlink)[0]
            if tlink.startswith('/'):
                tlink = 'http://thoptv.stream' + tlink
            if 'thoptv.' in tlink:          
                if 'dt.php' in tlink:
                    stream_url = re.findall('source\s*src\s*=\s*"([^"]+)',html)[0]
                elif '_Yupp.php' in tlink:
                    html = requests.get(tlink, headers=self.hdr).text
                    slink = re.findall('link="([^"]+)',html)[0]
                    headers = self.hdr
                    headers['Referer'] = tlink
                    thtml = requests.get('http://thoptv.com/_fYfrMihRme9XrzZ.php', headers=headers).text
                    tokpg = thtml.replace(';','\n').replace('var ','').replace('__T__T__T__','concat').replace('__T__T__','b').replace('push','append')
                    values = re.findall('(.*)\n',tokpg)
                    for value in values:
                        exec(value)
                    token = ''.join(concat(__O__3__P__, __T__1__H__, __H__2__O__))
                    stream_url = slink + token + '|User-Agent=%s'%self.hdr['User-Agent']
                    if 'hmac' not in token:
                        xbmc.log('No hmac in %s\n'%stream_url,xbmc.LOGNOTICE)
                        stream_url = 'http://content.jwplatform.com/videos/7RtXk3vl-52qL9xLP.mp4'

                else:
                    thlink = 'http://thoptv.stream/koZ4lxq2kN8hxEpHzlUa13WJM.php'
                    headers = self.hdr
                    headers['Referer'] = tlink
                    thtml = requests.get(thlink, headers=headers).text.replace(';','\n')
                    values = re.findall('([^\s]+\s=\s[^\n]+)',thtml)
                    for value in values:
                        exec(value)
                    token = '?jct=%s&pxe=%s&st=%s'%(uFmi,FAKL,QFYM)                        
                    cid = re.findall('channel=([^&]+)',tlink)[0]
                    streamer = random.choice(['sjpurcdnems01','sjpurcdnems02',
                                              'sambdcdnems01','sambdcdnems02','sambdcdnems03',
                                              'sbbsrcdnems01','sbbsrcdnems02','sbbsrcdnems03','sbbsrcdnems04',
                                              'sbbsrcdnems05','sbbsrcdnems06','sbbsrcdnems07','sbbsrcdnems08',
                                              'smumcdnems01','smumcdnems02','smumcdnems03','smumcdnems04',
                                              'ssrigcdnems01','ssrigcdnems02','ssrigcdnems03',
                                              'ssrigcdnems04','ssrigcdnems05','ssrigcdnems06',
                                              'sngprcdnems01','sngprcdnems02','sngprcdnems03',
                                              'sptnacdnems01','sptnacdnems02','sptnacdnems03',
                                              'sklktcdnems01','sklktcdnems02','sklktcdnems03','sklktcdnems04',
                                              'sklktcdnems05','sklktcdnems06','sklktcdnems07'])
                    stream_url = 'http://%s.cdnsrv.jio.com/jiotv.live.cdn.jio.com/%s/%s_%s.m3u8%s|User-Agent=%s'%(streamer,cid,cid,self.bitrate,token,self.jhdr['User-Agent'])
                    #stream_url = 'https://jiotvweb.cdn.jio.com/jiotv.live.cdn.jio.com/%s/%s_%s.m3u8%s|User-Agent=%s&X-Requested-With=com.jio.jioplay.tv'%(cid,cid,self.bitrate,token,self.jhdr['User-Agent'])


            elif 'gohellotv.' in tlink:
                html = requests.get(tlink, headers=self.hdr).text
                stream_url = re.findall('var\sdelivery\s*=\s*"([^"]+)',html)[0]
            elif ('dacast.' in tlink) or ('streamingasaservice.' in tlink):
                surl = tlink.split('.com')[1]
                headers = self.hdr
                headers['Referer'] = 'http://iframe.dacast.com/'
                act_data = requests.get('http://json.dacast.com' + surl, headers=headers).json()
                try:
                    act_url = act_data['hls']
                    if 'http' not in act_url:
                        act_url = 'http:' + act_url
                    act_data = requests.get('https://services.dacast.com/token/i%s?'%surl, headers=headers, verify=False).json()
                    new_token = act_data['token']
                    stream_url = act_url + new_token
                except:
                    stream_url = act_data['rtmp']
            elif 'zecast.' in tlink and '.m3u8' not in tlink:
                html = requests.get(tlink, headers=self.hdr, verify=False).text
                stream_url = re.findall('class="container"\s*src="([^"]+)',html)[0]
            elif '.m3u8' in tlink:
                stream_url = tlink + '|User-Agent=%s'%self.hdr['User-Agent']
            else:
                xbmc.log('%s not resolvable.\n'%tlink,xbmc.LOGNOTICE)

                       
        return stream_url