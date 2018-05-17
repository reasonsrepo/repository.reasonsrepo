'''
Base deccandelight Scraper class
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

import xbmc, xbmcaddon
import json, re, requests, urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
from resources.lib import jsunpack
import resolveurl

_addon = xbmcaddon.Addon()
_addonname = _addon.getAddonInfo('name')
_version = _addon.getAddonInfo('version')
_addonID = _addon.getAddonInfo('id')
_icon = _addon.getAddonInfo('icon')
_fanart = _addon.getAddonInfo('fanart')
_path = _addon.getAddonInfo('path')
_ipath = _path + '/resources/images/'
_settings = _addon.getSetting
_timeout = _settings('timeout')

mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
ioshdr = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A402 Safari/604.1'}
droidhdr = {'User-Agent': 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; MI 5 Build/KTU84P)'}
jiohdr = {'User-Agent': 'ExoPlayerDemo/5.2.0 (Linux;Android 6.0.1) ExoPlayerLib/2.3.0'}

class Scraper(object):
    
    def __init__(self):
        self.ipath = _ipath
        self.hdr = mozhdr
        self.dhdr = droidhdr
        self.jhdr = jiohdr
        self.ihdr = ioshdr
        self.settings = _settings
        self.adult = _settings('adult')
        self.nicon = self.ipath + 'next.png'
        
    def get_nicon(self):
        return self.nicon
    
    def get_SearchQuery(self,sitename):
        keyboard = xbmc.Keyboard()
        keyboard.setHeading('Search ' + sitename)
        keyboard.doModal()
        if keyboard.isConfirmed():
            search_text = keyboard.getText()

        return search_text

    def get_vidhost(self,url):
        """
        Trim the url to get the video hoster
        :return vidhost
        """
        parts = url.split('/')[2].split('.')
        vidhost = '%s.%s'%(parts[len(parts)-2],parts[len(parts)-1])
        return vidhost

    def resolve_media(self,url,videos,vidtxt=''):
        non_str_list = ['olangal.', '#', 'magnet:', 'desihome.', 'thiruttuvcd',
                        'cineview', 'bollyheaven', 'videolinkz', 'moviefk.co', 'goo.gl',
                        'imdb.', 'mgid.', 'atemda.', 'movierulz.', 'facebook.',
                        'm2pub', 'abcmalayalam', 'india4movie.co', '.filmlinks4u',
                        'tamilraja.', 'multiup.', 'filesupload.', 'fileorbs.', 'tamil.ws',
                        'insurance-donate.', '.blogspot.', 'yodesi.net', 'desi-tashan.',
                        'yomasti.co/ads', 'ads.yodesi', '/ads/', 'mylifeads.']

        embed_list = ['cineview', 'bollyheaven', 'videolinkz', 'vidzcode', 
                      'embedzone', 'embedsr', 'fullmovie-hd', 'links4.pw',
                      'embedscr', 'embedrip', 'movembed', 'power4link.us',
                      'watchmoviesonline4u', 'nobuffer.info', 'yomasti.co',
                      'techking.me', 'onlinemoviesworld.xyz', 'cinebix.com',
                      'desihome.', 'loan-forex.', 'filmshowonline.', 'vids.xyz',
                      'business-tv.me', 'telly-news.', 'tellytimes.', 'techking.',
                      'adly.biz', 'business-', 'businessvoip.', 'toptencar.',
                      'loanadvisor.']
           
        if 'filmshowonline.net/media/' in url:
            try:
                r = requests.get(url, headers=self.hdr)
                clink = r.text
                cookies = r.cookies
                eurl = re.findall("var height.*?url: '(.*?)'", clink, re.DOTALL)[0]
                enonce = re.findall("var height.*?nonce.*?'(.*?)'", clink, re.DOTALL)[0]
                evid = re.findall("var height.*?link_id: ([^\s]*)", clink, re.DOTALL)[0]
                values = {'echo' : 'true',
                          'nonce' : enonce,
                          'width' : '848',
                          'height' : '480',
                          'link_id' : evid }
                headers = self.hdr
                headers['Referer'] = url
                headers['X-Requested-With'] = 'XMLHttpRequest'
                emurl = requests.post(eurl, data=values, headers=headers, cookies=cookies).text
                strurl = (re.findall('(http[^"]*)', emurl)[0]).replace('\\', '')
                if resolveurl.HostedMediaFile(strurl):
                    vidhost = self.get_vidhost(strurl)
                    if not vidtxt == '':
                        vidhost += ' | %s' % vidtxt
                    videos.append((vidhost,strurl))
            except:
                pass

        elif 'justmoviesonline.com' in url:
            html = requests.get(url, headers=mozhdr).text
            src = re.search("atob\('(.*?)'",html)
            if src:
                src = src.group(1)
                try:
                    strurl = re.findall('file":"(.*?)"',src.decode('base64'))[0]
                    vidhost = 'GVideo'
                    strurl = urllib.quote_plus(strurl)
                    videos.append((vidhost,strurl))
                except:
                    pass
                try:
                    strurl = re.findall('''source src=["'](.*?)['"]''',src.decode('base64'))[0]
                    vidhost = self.get_vidhost(strurl)
                    videos.append((vidhost,strurl))
                except:
                    pass
            elif '?id=' in url:
                src = eval(re.findall('Loading.+?var.+?=([^;]+)',html,re.DOTALL)[0])
                for item in src:
                    if 'http' in item and 'justmovies' not in item:
                        strurl = item
                strurl += url.split('?id=')[1]
                strurl += '.mp4|User-Agent=%s'%mozhdr['User-Agent']
                vidhost = 'GVideo'
                strurl = urllib.quote_plus(strurl)
                videos.append((vidhost,strurl))
            
        elif 'videohost.site' in url or 'videohost1.com' in url:
            try:
                html = requests.get(url, headers=mozhdr).text
                pdata = eval(re.findall('Run\((.*?)\)',html)[0]).decode('base64')
                linkcode = jsunpack.unpack(pdata).replace('\\','')
                sources = json.loads(re.findall('sources:(.*?\}\])',linkcode)[0])
                for source in sources:    
                    strurl = source['file'] + '|Referer=%s'%url
                    vidhost = self.get_vidhost(url) + ' | GVideo | %s' % source['label']
                    strurl = urllib.quote_plus(strurl)
                    videos.append((vidhost,strurl))
            except:
                pass

        elif 'videohost2.com' in url:
            html = requests.get(url, headers=mozhdr).text
            
            try:
                pdata = eval(re.findall('Loading video.+?(\[.+?\]);',html,re.DOTALL)[0])
                if 'id=' in url:
                    strurl = pdata[7] + url.split('=')[1] + pdata[9]
                else:    
                    strurl = pdata[7]
                vidhost = self.get_vidhost(url) + ' | GVideo'
                strurl = urllib.quote_plus(strurl + '|Referer=%s'%url)
                videos.append((vidhost,strurl))
            except:
                pass
            
            try:
                pdata = re.findall("atob\('([^']+)",html)[0].decode('base64')
                strurl = re.findall("source\ssrc='([^']+)",pdata)[0] + '|Referer=%s'%url
                vidhost = self.get_vidhost(url)
                strurl = urllib.quote_plus(strurl)
                videos.append((vidhost,strurl))
            except:
                pass
                
        elif 'tamildbox' in url:
            link = requests.get(url, headers=mozhdr).text
            try:
                mlink = SoupStrainer('div', {'id':'player-embed'})
                dclass = BeautifulSoup(link, parseOnlyThese=mlink)       
                if 'unescape' in str(dclass):
                    etext = re.findall("unescape.'[^']*", str(dclass))[0]
                    etext = urllib.unquote(etext)
                    dclass = BeautifulSoup(etext)
                glink = dclass.iframe.get('src')
                if resolveurl.HostedMediaFile(glink):
                    vidhost = self.get_vidhost(glink)
                    videos.append((vidhost,glink))
            except:
                pass    
            
            try:
                mlink = SoupStrainer('div', {'class':re.compile('^item-content')})
                dclass = BeautifulSoup(link, parseOnlyThese=mlink)
                glink = dclass.p.iframe.get('src')
                if resolveurl.HostedMediaFile(glink):
                    vidhost = self.get_vidhost(glink)
                    videos.append((vidhost,glink))
            except:
                pass
                
            try:
                if 'p,a,c,k,e,d' in link:
                    linkcode = jsunpack.unpack(link).replace('\\','')
                    glink = re.findall("file\s*:\s*'(.*?)'",linkcode)[0]
                if 'youtu.be' in glink:
                    glink = 'https://docs.google.com/vt?id=' + glink[16:]
                if resolveurl.HostedMediaFile(glink):
                    vidhost = self.get_vidhost(glink)
                    videos.append((vidhost,glink))
            except:
                pass

            try:
                codes = re.findall('"return loadEP.([^,]*),(\d*)',link)
                for ep_id, server_id in codes:
                    burl = 'http://www.tamildbox.com/actions.php?case=loadEP&ep_id=%s&server_id=%s'%(ep_id,server_id)
                    bhtml = requests.get(burl,headers=mozhdr).text
                    blink = re.findall('(?i)iframe\s*src="(.*?)"',bhtml)[0]
                    vidhost = self.get_vidhost(blink)
                    if 'googleapis' in blink:
                        blink = 'https://drive.google.com/open?id=' + re.findall('docid=([^&]*)',blink)[0]
                        vidhost = 'GVideo'
                    videos.append((vidhost,blink))   
            except:
                pass
            
        elif any([x in url for x in embed_list]):
            clink = requests.get(url, headers=mozhdr).text
            csoup = BeautifulSoup(clink)
            try:
                links = re.findall('''(?i)<iframe.+?src=["']([^'"]+)''', clink)
                for strurl in links:
                    #xbmc.log('-------> Scraped link : %s' % strurl, xbmc.LOGNOTICE)
                    if not any([x in strurl for x in non_str_list]):
                        #xbmc.log('-------> sending to resolveurl for checking : %s' % strurl, xbmc.LOGNOTICE)
                        if resolveurl.HostedMediaFile(strurl):
                            vidhost = self.get_vidhost(strurl)
                            if not vidtxt == '':
                                vidhost += ' | %s' % vidtxt
                            videos.append((vidhost,strurl))
                        else:
                            xbmc.log('-------> resolveurl cannot resolve : %s'%strurl, xbmc.LOGNOTICE)
            except:
                pass

            try:
                plink = csoup.find('a', {'class':'main-button dlbutton'})
                strurl = plink.get('href')
                if not any([x in strurl for x in non_str_list]):
                    if resolveurl.HostedMediaFile(strurl):
                        vidhost = self.get_vidhost(strurl)
                        if not vidtxt == '':
                            vidhost += ' | %s' % vidtxt
                        videos.append((vidhost,strurl))
            except:
                pass

            try:
                plink = csoup.find('div', {'class':'aio-pulse'})
                strurl = plink.find('a')['href']
                if not any([x in strurl for x in non_str_list]):
                    if resolveurl.HostedMediaFile(strurl):
                        vidhost = self.get_vidhost(strurl)
                        if not vidtxt == '':
                            vidhost += ' | %s' % vidtxt
                        videos.append((vidhost,strurl))
            except:
                pass

            try:
                plink = csoup.find('div', {'class':re.compile('entry-content')})
                strurl = plink.find('a')['href']
                if not any([x in strurl for x in non_str_list]):
                    if resolveurl.HostedMediaFile(strurl):
                        vidhost = self.get_vidhost(strurl)
                        if not vidtxt == '':
                            vidhost += ' | %s' % vidtxt
                        videos.append((vidhost,strurl))
            except:
                pass

            try:
                for linksSection in csoup.findAll('embed'):
                    strurl = linksSection.get('src')
                    if not any([x in strurl for x in non_str_list]):
                        if resolveurl.HostedMediaFile(strurl):
                            vidhost = self.get_vidhost(strurl)
                            if not vidtxt == '':
                                vidhost += ' | %s' % vidtxt
                            videos.append((vidhost,strurl))
            except:
                pass
                
        elif not any([x in url for x in non_str_list]):
            if resolveurl.HostedMediaFile(url):
                vidhost = self.get_vidhost(url)
                if not vidtxt == '':
                    vidhost += ' | %s' % vidtxt
                videos.append((vidhost,url))
            else:
                xbmc.log('-------> ResolveUrl cannot resolve : %s'%url, xbmc.LOGNOTICE)

        return
        
    def clean_title(self, title):
        cleanup = ['Watch Online Movie', 'Watch Onilne', 'Tamil Movie ', 'Tamil Dubbed', 'WAtch ', 'Online Free',
                   'Full Length', 'Latest Telugu', 'RIp', 'DvDRip', 'DvDScr',
                   'Full Movie Online Free', 'Full Movie Online', 'Watch Online ', 'Free HD', 'Online Full Movie',
                   'Full Free', 'Malayalam Movie', ' Malayalam ', 'Full Movies', 'Full Movie', 'Free Online',
                   'Movie Online', 'Watch ', 'movie online', 'Wach ', 'Movie Songs Online', 'Full Hindi',
                   'tamil movie songs online', 'tamil movie songs', 'movie songs online', 'Tamil Movie', ' Hindi',
                   'Hilarious Comedy Scenes', 'Super Comedy Scenes', 'Ultimate Comedy Scenes', 'Watch...',
                   'Super comedy Scenes', 'Comedy Scenes', 'hilarious comedy Scenes', '...', 'Telugu Movie',
                   'Sun TV Show', 'Vijay TV Show', 'Vijay Tv Show', 'Vijay TV Comedy Show', 'Hindi Movie',
                   'Vijay Tv Comedy Show', 'Vijay TV', 'Vijay Tv', 'Sun Tv Show', 'Download', 'Starring', u'\u2013',
                   'Tamil Full Movie', 'Tamil Horror Movie', 'Tamil Dubbed Movie', '|', '-', ' Full ', u'\u2019',
                   '/', 'Pre HDRip', '(DVDScr Audio)', 'PDVDRip', 'DVDSCR', '(HQ Audio)', 'HQ', ' Telugu',
                   'DVDScr', 'DVDscr', 'PreDVDRip', 'DVDRip', 'DVDRIP', 'WEBRip', 'WebRip', 'Movie', ' Punjabi',
                   'TCRip', 'HDRip', 'HDTVRip', 'HD-TC', 'HDTV', 'TVRip', '720p', 'DVD', 'HD', ' Dubbed', '( )',
                   '720p', '(UNCUT)', 'UNCUT', '(Clear Audio)', 'DTHRip', '(Line Audio)', ' Kannada', ' Hollywood',
                   'TS', 'CAM', 'Online Full', '[+18]', 'Streaming Free', 'Permalink to ', 'And Download', '()',
                   'Full English', ' English', 'Downlaod', 'Bluray', 'Online', ' Tamil', ' Bengali', ' Bhojpuri']
        
        for word in cleanup:
            if word in title:
                title = title.replace(word,'')

        title = title.strip()
        title = title.encode('utf8')
        return title
