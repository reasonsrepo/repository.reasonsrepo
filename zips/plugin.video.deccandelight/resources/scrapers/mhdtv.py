'''
mhdtvlive deccandelight plugin
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
import urllib, re, requests, time
from resources.lib import cfscrape
import xbmc, xbmcgui
import HTMLParser
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
cache = StorageServer.StorageServer('deccandelight', 1)

class mhdtv(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://mhdtvlive.stream/'
        self.icon = self.ipath + 'mhdtv.png'
        self.qvalues = ['Low','Med','Default','Good','High']
        self.bvalues = ['250','400','600','800','1200']
        self.qual = self.qvalues[int(self.settings('thopqual'))]
        self.bitrate = self.bvalues[int(self.settings('thopqual'))]
        self.list = {'01Tamil TV': 'tamilMMMM5',
                     '02Telugu TV': self.bu + 'language/telugu/',
                     '03Malayalam TV': 'malayalamMMMM5',
                     '04Kannada TV': self.bu + 'language/kannada/',
                     '05Hindi TV': 'hindiMMMM5',
                     '06English TV': 'englishMMMM5',
                     '07Sports TV': self.bu + 'language/sports/',
                     '08Marathi TV': self.bu + 'language/marathi-channels/',
                     '09Punjabi TV': self.bu + 'language/punjabi/',
                     '10Bangla TV': self.bu + 'language/bangla-channels/',
                     '11Sinhala TV': self.bu + 'language/sinhala-channels/'}

    def get_login(self):
        usr = self.settings('mhdusr')
        pwd = self.settings('mhdpwd')
        durl = self.bu + 'wp-includes/js/wp-embed.min.js'
        lurl = self.bu + 'wp-login.php'
        cj = cfscrape.get_tokens(durl,user_agent=self.hdr['User-Agent'])[0]
        if len(usr) < 1 or len(pwd) < 1:
            xbmcgui.Dialog().ok('MHDTV Settings','Setup Username and Password in Settings!')
            self.list = {}
            return
        data = {'log':usr,
                'pwd':pwd,
                'wp-submit':'Log In',
                'redirect_to':self.bu,
                'action':'vt_ajax_login',
                'button_label':'Log In'}
        resp = requests.post(lurl,data=data,headers=self.hdr,cookies=cj,allow_redirects=False)
        lcj = requests.utils.dict_from_cookiejar(resp.cookies)
        try:
            lcj['cf_clearance'] = cj['cf_clearance']
        except:
            pass
        ckstr = '; '.join([str(x)+"="+str(y) for x,y in lcj.items()])
        return (lcj,ckstr)
            
    def get_menu(self):
        return (self.list,7,self.icon)

    def get_second(self,iurl):
        """
        Get the list of dates.
        :return: list
        """
        cats = {'tamil': {'01Entertainment': self.bu + 'language/tamil/',
                          '02Local': self.bu + 'language/tamil-local/',
                          '03News': self.bu + 'language/tamil-news/'},
                'malayalam': {'01Entertainment': self.bu + 'language/malayalam/',
                              '02Local': self.bu + 'language/malayalam-local/',
                              '03News': self.bu + 'language/malayalam-news/',
                              '04Devotional': self.bu + 'language/malayalam-devotional/'},
                'hindi': {'01Entertainment': self.bu + 'language/hindi/',
                          '02Movies': self.bu + 'language/hindi-movie-channels/',
                          '03Music': self.bu + 'language/hindi-music/',
                          '04News': self.bu + 'language/hindi-news/',
                          '05Devotional': self.bu + 'language/hindi-devotional/'},
                'english': {'01Entertainment': self.bu + 'language/english/',
                            '02Fashion': self.bu + 'language/fashion-channels/',
                            '03News': self.bu + 'language/english-news/'}}

        categories = []

        for title,url in sorted(cats[iurl].iteritems()):
            categories.append((title[2:],self.icon,url))   
        
        return (categories,7)
        
    def get_items(self,iurl):
        cj,ckstr = cache.cacheFunction(self.get_login)
        channels = []
        h = HTMLParser.HTMLParser()
        mlink = SoupStrainer('article', {'class':'item'})
        plink = SoupStrainer('div', {'class':'resppages'})
        nextpg = True
        while nextpg:
            html = requests.get(iurl, cookies=cj, headers=self.hdr).text
            Paginator = BeautifulSoup(html, parseOnlyThese=plink)
            items = BeautifulSoup(html, parseOnlyThese=mlink)
            for item in items:
                title = h.unescape(item.h3.text).encode('utf8')
                url = item.find('a')['href']
                thumb = item.find('img')['src'] + '|User-Agent=%s&Cookie=%s'%(self.hdr['User-Agent'],ckstr)
                channels.append((title.title(), thumb, url))
            if 'chevron-right' in str(Paginator):
                iurl = Paginator.find('a')['href']
            else:
                nextpg = False  
        return (sorted(channels),9) 

    def get_video(self,url):
        cj,ckstr = cache.cacheFunction(self.get_login)        
        html = requests.get(url, cookies=cj, headers=self.hdr).text
        tlink = re.findall('iframe[^>]+src="([^"]+)',html)[0]
        if 'http' not in tlink:
            tlink = self.bu[:-1] + tlink
        if 'mhdtvlive.' in tlink or 'livemalayalamtv.' in tlink:
            headers = self.hdr
            headers['Referer'] = url
            html = requests.get(tlink, cookies=cj, headers=headers).text
            if 'unescape(' in html:
                strdata = re.findall("unescape\(\s*'(.*?)'", html)[0]
                stream_url = urllib.unquote(strdata)
                if 'http' not in stream_url:
                    stream_url = self.bu[:-1] + stream_url + '|User-Agent=%s&Cookie=%s'%(self.hdr['User-Agent'],ckstr)
                else:
                    stream_url += '|User-Agent=%s'%self.hdr['User-Agent']
            elif 'androidhls": true' in html and 'akamaihd' in html:
                stream_url = re.findall('stream = "([^"]+)',html)[0]
                stream_url += '|User-Agent=%s'%self.hdr['User-Agent']
            elif 'stream =' in html:
                stream_url = re.findall('stream = "(.*?)"',html)[0]
            elif 'sv = "' in html:
                stream_url = re.findall('sv\s*=\s*"(.*?)"',html)[0]
            elif 'vodobox.' in html:
                stream_url = urllib.unquote(re.findall('vid=([^&]+)',html)[0])
            elif 'nexgtv.' in html:
                nlink = re.findall('iframe.+src="([^"]+)',html)[0]
                html = requests.get(nlink, headers=self.hdr).text
                chid = re.findall("getSecurePlayUrl\('([^']+)",html)[0]
                surl = 'https://m.nexgtv.com/users/getsecureplayurl/%s?_=%s'%(chid,int(round(time.time() * 1000)))
                html = requests.get(surl, headers=self.hdr).json()
                surl = html['finalUrl']
                html = requests.get(surl, headers=self.hdr).text
                stream_url = re.findall('(http.+)',html)[-1]
            elif 'fp-hlsjs' in html:
                pars = re.findall('flowplayer.+src:((.+?)\[[^}]+)',html)[0]
                exec(re.findall('var\s*(%s=.+?);'%pars[1],html)[0])
                stream_url = self.bu[:-1] + eval(pars[0]) + '|User-Agent=%s&Cookie=%s'%(self.hdr['User-Agent'],ckstr)
            elif 'watermark:_' in html:
                pars = re.findall('Clappr.+?source:((.+?)\[.+?),',html)[0]
                exec(re.findall('var\s*(%s=.+?);'%pars[1],html)[0])
                stream_url = eval(pars[0]) + '|User-Agent=%s'%self.hdr['User-Agent']
            elif 'hls.loadSource' in html:
                stream_url = re.findall("loadSource\('([^']+)",html)[0] + '|User-Agent=%s&Cookie=%s'%(self.hdr['User-Agent'],ckstr)
            else:
                stream_url = re.findall("source:\s*'([^']+)",html)[0] + '|User-Agent=%s&Cookie=%s'%(self.hdr['User-Agent'],ckstr)
        elif 'yupptv.' in tlink or 'apktv.' in tlink:
            html = requests.get(tlink, headers=self.hdr, verify=False).text
            stream_url = re.findall("(?:file|source):\s?'(.*?m3u8.*?)'",html)[0]
            r = requests.get(stream_url,headers=self.hdr, verify=False)
            stream_url = re.findall('(http.*)',r.text)[-1]
            stream_url += '|User-Agent=%s&Cookie=_alid_=%s'%(self.hdr['User-Agent'],r.cookies['_alid_'])
        elif 'youtube.' in tlink:
            stream_url = tlink
        elif '.php' in tlink:
            html = requests.get(tlink, headers=self.hdr).text
            stream_url = re.findall('file:\s*"([^"]+)',html)[0]
        else:
            xbmc.log('%s not resolvable.\n'%tlink,xbmc.LOGNOTICE)
            stream_url = ''
        
        if ('yupp' in stream_url or 'akamaized' in stream_url) and 'User-Agent' not in stream_url:
            stream_url += '|User-Agent=%s'%self.hdr['User-Agent']
        #xbmc.log('@@@@Stream_url is %s\n'%stream_url,xbmc.LOGNOTICE)
        return stream_url