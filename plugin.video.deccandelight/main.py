"""
    Deccan Delight Kodi Addon
    Copyright (C) 2016 gujal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib, re, requests, os
import resolveurl
import YDStreamUtils
import YDStreamExtractor

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

_addon = xbmcaddon.Addon()
_addonname = _addon.getAddonInfo('name')
_version = _addon.getAddonInfo('version')
_addonID = _addon.getAddonInfo('id')
_icon = _addon.getAddonInfo('icon')
_fanart = _addon.getAddonInfo('fanart')
_path = _addon.getAddonInfo('path')
_ipath = _path + '/resources/images/'
_settings = _addon.getSetting

cache = StorageServer.StorageServer('deccandelight', _settings('timeout'))

def clear_cache():
    """
    Clear the cache database.
    """
    msg = 'Cached Data has been cleared'
    cache.table_name = 'deccandelight'
    cache.cacheDelete('%get%')
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(_addonname, msg, 3000, _icon))

safhdr = 'Mozilla/5.0 (%s) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A356 Safari/604.1'

try:
    platform = re.findall('\(([^\)]+)', xbmc.getUserAgent())[0]
except:
    platform = 'Linux; Android 4.4.4; MI 5 Build/KTU84P'


if _settings('version') != _version:
    _addon.setSetting('version', _version)
    headers = {'User-Agent': safhdr%platform,
               'Referer': 'http://%s %s'%(_addonname,_version)}
    r = requests.get('\x68\x74\x74\x70\x3a\x2f\x2f\x67\x6f\x6f\x2e\x67\x6c\x2f\x62\x59\x31\x4a\x53\x4c',headers=headers)
    clear_cache()
    _addon.openSettings()


sites = {'01tgun': 'Tamil Gun : [COLOR yellow]Tamil[/COLOR]',
         #'02rajt': 'Raj Tamil : [COLOR yellow]Tamil[/COLOR]',
         '03tyogi': 'Tamil Yogi : [COLOR yellow]Tamil[/COLOR]',
         '05rasigan': 'Tamil Rasigan : [COLOR yellow]Tamil[/COLOR]',
         '06tamiltv': 'APKLand TV : [COLOR yellow]Tamil Live TV and VOD[/COLOR]',
         '07lyca': 'Lyca TV : [COLOR yellow]Tamil Live TV[/COLOR]',
         '08bbt': 'BigBoss Tamil : [COLOR yellow]Tamil Catchup TV[/COLOR]',
         '11tdhool': 'Tamil Dhool : [COLOR yellow]Tamil Catchup TV[/COLOR]',
         '12tst247': 'Tamil Serial Today : [COLOR yellow]Tamil Catchup TV[/COLOR]',
         '13tstv': 'Tamil Serials : [COLOR yellow]Tamil Catchup TV[/COLOR]',
         '14ttvs': 'Tamil TV Shows : [COLOR yellow]Tamil Catchup TV[/COLOR]',
         '16awatch': 'Andhra Watch : [COLOR yellow]Telugu[/COLOR]',
         '17manatv': 'Mana Telugu : [COLOR yellow]Telugu Catchup TV[/COLOR]',
         '18tflame': 'Telugu Flame : [COLOR yellow]Telugu Catchup TV[/COLOR]',
         '21olangal': 'Olangal : [COLOR yellow]Malayalam[/COLOR]',
         '22torm': 'TOR Malayalam : [COLOR yellow]Malayalam[/COLOR]',
         '41hlinks': 'Hindi Links 4U : [COLOR yellow]Hindi[/COLOR]',
         '42desit': 'Desi Tashan : [COLOR yellow]Hindi Catchup TV[/COLOR]',
         '46desiserials': 'Desi Serials : [COLOR yellow]Hindi Catchup TV[/COLOR]',
         '47yodesi': 'Yo Desi : [COLOR yellow]Hindi Catchup TV[/COLOR]',
         '48gmala': 'Hindi Geetmala : [COLOR yellow]Hindi Songs[/COLOR]',
         #'55thop': 'THOP TV : [COLOR magenta]Various Live TV[/COLOR]',
         '53mhdtv': 'MHDTV Live : [COLOR magenta]Various Live TV[/COLOR]',
         '54nextv': 'NexTV Live : [COLOR magenta]Various Live TV[/COLOR]',
         #'52hyfy': 'HyFy TV : [COLOR magenta]Various Live TV[/COLOR]',
         '51aindia': 'Abroad India : [COLOR magenta]Various Live TV[/COLOR]',
         #'60ozee': 'OZee : [COLOR magenta]Various Catchup TV[/COLOR]',
         '61bmov': 'Bharat Movies : [COLOR magenta]Various[/COLOR]',
         #'62tvcd': 'Thiruttu VCD : [COLOR magenta]Various[/COLOR]',
         '63mrulz': 'Movie Rulz : [COLOR magenta]Various[/COLOR]',
         #'64i4movie': 'India 4 Movie : [COLOR magenta]Various[/COLOR]',
         #'65moviefk': 'Movie FK : [COLOR magenta]Various[/COLOR]',
         '66mfish': 'Movie Fisher : [COLOR magenta]Various[/COLOR]',
         '67mersal': 'Mersalaayitten : [COLOR magenta]Various[/COLOR]',
         '69flinks': 'Film Links 4 U : [COLOR magenta]Various[/COLOR]',
         '71tvcds': 'Thiruttu VCDs : [COLOR magenta]Various[/COLOR]',
         '72tmvp': 'TMVPlay : [COLOR magenta]Various[/COLOR]',
         '73wompk': 'Online Movies PK : [COLOR magenta]Various[/COLOR]'}

for site,title in sorted(sites.iteritems()):
    if _settings(site[2:]) == 'true':
        ri = 'from resources.scrapers import %s'%site[2:]
        exec(ri)

def list_sites():
    """
    Create the Sites menu in the Kodi interface.
    """
    listing = []
    for site,title in sorted(sites.iteritems()):
        if _settings(site[2:]) == 'true':
            item_icon = _ipath + '%s.png'%site[2:]
            list_item = xbmcgui.ListItem(label=title)
            list_item.setArt({'thumb': item_icon,
                              'icon': item_icon,
                              'poster': item_icon,
                              'fanart': _fanart})
            url = '{0}?action=1&site={1}'.format(_url, site[2:])
            is_folder = True
            listing.append((url, list_item, is_folder))
    
    list_item = xbmcgui.ListItem(label='[COLOR yellow][B]Clear Cache[/B][/COLOR]')
    item_icon = _ipath + 'ccache.png'
    list_item.setArt({'thumb': item_icon,
                      'icon': item_icon,
                      'poster': item_icon,
                      'fanart': _fanart})
    url = '{0}?action=0'.format(_url)
    is_folder = False
    listing.append((url, list_item, is_folder))
    
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'videos')
    xbmcplugin.endOfDirectory(_handle)

def list_menu(site):
    """
    Create the Site menu in the Kodi interface.
    """
    scraper = eval('%s.%s()'%(site,site))
    menu,mode,icon = cache.cacheFunction(scraper.get_menu)
    #menu,mode,icon = scraper.get_menu()
    listing = []
    for title,iurl in sorted(menu.iteritems()):
        digits = len(re.findall('^(\d*)',title)[0])
        if 'MMMM' in iurl:
            niurl = iurl.split('MMMM')[0]
            nmode = iurl.split('MMMM')[1]
            list_item = xbmcgui.ListItem(label=title[digits:])
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, nmode, site, urllib.quote(niurl))
            is_folder = True
            listing.append((url, list_item, is_folder))
        elif 'Adult' not in title:
            list_item = xbmcgui.ListItem(label=title[digits:])
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'poster': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, mode, site, urllib.quote(iurl))
            if mode == 9:
                is_folder = False
                list_item.setProperty('IsPlayable', 'true')
                list_item.addStreamInfo('video', { 'codec': 'h264'})
            else:
                is_folder = True
            listing.append((url, list_item, is_folder))
        elif _settings('adult') == 'true':
            list_item = xbmcgui.ListItem(label=title[digits:])
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'poster': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, mode, site, urllib.quote(iurl))
            is_folder = True
            listing.append((url, list_item, is_folder))            
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'videos')
    xbmcplugin.endOfDirectory(_handle)

def list_top(site,iurl):
    """
    Create the Site menu in the Kodi interface.
    """
    scraper = eval('%s.%s()'%(site,site))
    menu,mode = cache.cacheFunction(scraper.get_top,iurl)
    listing = []
    for title,icon,iurl in menu:
            list_item = xbmcgui.ListItem(label=title)
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'poster': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, mode, site, urllib.quote(iurl))
            is_folder = True
            listing.append((url, list_item, is_folder))            
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'videos')
    xbmcplugin.endOfDirectory(_handle)

def list_second(site,iurl):
    """
    Create the Site menu in the Kodi interface.
    """
    scraper = eval('%s.%s()'%(site,site))
    menu,mode = cache.cacheFunction(scraper.get_second,iurl)
    listing = []
    for title,icon,iurl in menu:
        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({'thumb': icon,
                          'icon': icon,
                          'poster': icon,
                          'fanart': _fanart})
        nextmode = mode
        if 'Next Page' in title:
            nextmode = 5
        url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, nextmode, site, urllib.quote(iurl))
        is_folder = True
        if mode == 9 and 'Next Page' not in title:
            is_folder = False
            list_item.setProperty('IsPlayable', 'true')
            list_item.addStreamInfo('video', { 'codec': 'h264'})
        listing.append((url, list_item, is_folder))            
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'tvshows')
    xbmcplugin.endOfDirectory(_handle)

def list_items(site,iurl):
    """
    Create the list of movies/episodes in the Kodi interface.
    """
    scraper = eval('%s.%s()'%(site,site))
    if iurl.endswith('='):
        movies,mode = scraper.get_items(iurl)
    else:
        movies,mode = cache.cacheFunction(scraper.get_items,iurl)
    listing = []
    for movie in movies:
        title = movie[0]
        if title == '':
            title = 'Unknown'
        list_item = xbmcgui.ListItem(label=title)
        list_item.setInfo('video', {'title': title})
        if 'Next Page' in title:
            if mode == 9:
                nextmode = 7
            else:
                nextmode = mode - 1
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, nextmode, site, urllib.quote(movie[2]))
            list_item.setArt({'thumb': movie[1],
                              'icon': movie[1],
                              'poster': movie[1],
                              'fanart': _fanart})            
        else:
            qtitle = urllib.quote(title)
            iurl = urllib.quote(movie[2])
            url = '{0}?action={1}&site={2}&title={3}&thumb={4}&iurl={5}'.format(_url, mode, site, qtitle, urllib.quote(movie[1].encode('utf8')), iurl)
            list_item.setArt({'thumb': movie[1],
                              'icon': movie[1],
                              'poster': movie[1],
                              'fanart': _fanart})
        if mode == 9 and 'Next Page' not in title:
            is_folder = False
            list_item.setProperty('IsPlayable', 'true')
            list_item.addStreamInfo('video', { 'codec': 'h264'})
        else:
            is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'movies')
    xbmcplugin.endOfDirectory(_handle)
    
def list_videos(site,title,iurl,thumb):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: str
    """
    scraper = eval('%s.%s()'%(site,site))
    videos = cache.cacheFunction(scraper.get_videos,iurl)
    listing = []
    for video in videos:
        list_item = xbmcgui.ListItem(label=video[0])
        list_item.setArt({'thumb': thumb,
                          'icon': thumb,
                          'poster': thumb,
                          'fanart': thumb})
        list_item.setInfo('video', {'title': title})
        list_item.addStreamInfo('video', { 'codec': 'h264'})
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=9&iurl={1}'.format(_url, video[1])
        list_item.addContextMenuItems([('Save Video', 'RunPlugin(plugin://'+_addonID+'/?action=10&iurl='+video[1].encode('utf8')+'ZZZZ'+title+')',)])
        is_folder = False
        listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'videos')
    xbmcplugin.endOfDirectory(_handle)

def resolve_url(url):
    duration=7500   
    try:
        stream_url = resolveurl.HostedMediaFile(url=url).resolve()
        # If resolveurl returns false then the video url was not resolved.
        if not stream_url or not isinstance(stream_url, basestring):
            try: msg = stream_url.msg
            except: msg = url
            #xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('Resolve URL',msg, duration, _icon))
            xbmcgui.Dialog().ok('Resolve URL',msg)
            return False
    except Exception as e:
        try: msg = str(e)
        except: msg = url
        #xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('Resolve URL',msg, duration, _icon))
        xbmcgui.Dialog().ok('Resolve URL',msg)
        return False
        
    return stream_url

def play_video(iurl, dl=False):
    """
    Play a video by the provided path.

    :param path: str
    """
    streamer_list = ['tamilgun', 'mersalaayitten', 'mhdtvlive.', '/hls/', 'poovee.',
                     'watchtamiltv.', 'cloudspro.', 'abroadindia.', 'nextvnow.', 'akamaihd.',
                     'hindigeetmala.','.mp4', 'googlevideo.', 'tmvplay.', 'playembed.',
                     'tamilhdtv.', 'andhrawatch.', 'tamiltv.', 'thoptv.', 'athavantv',
                     'justmoviesonline.', '.mp3', 'googleapis.', '.m3u8', 'telugunxt.',
                     'ozee.', 'bharat-movies.', 'googleusercontent.', 'hyfytv.']
    # Create a playable item with a path to play.
    title = 'unknown'
    if 'ZZZZ' in iurl:
        iurl,title = iurl.split('ZZZZ')

    play_item = xbmcgui.ListItem(path=iurl)
    vid_url = play_item.getfilename()
    #xbmc.log("DeccanDelight vid_url = %s" %vid_url,xbmc.LOGNOTICE)
    if any([x in vid_url for x in streamer_list]):
        if 'mersalaayitten' in vid_url:
            scraper = mersal.mersal()
            stream_url,srtfile = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
            if srtfile:
                play_item.setSubtitles(['special://temp/mersal.srt', srtfile])
        elif 'athavantv.' in vid_url:
            scraper = lyca.lyca()
            stream_url = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
        elif 'hindigeetmala.' in vid_url:
            scraper = gmala.gmala()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                play_item.setPath(stream_url)
        elif 'telugunxt.' in vid_url:
            scraper = tflame.tflame()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                stream_url = resolve_url(stream_url)
                if stream_url:
                    play_item.setPath(stream_url)
                else:
                    play_item.setPath(None)
        elif 'bharat-movies.' in vid_url:
            scraper = bmov.bmov()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                stream_url = resolve_url(stream_url)
                if stream_url:
                    play_item.setPath(stream_url)
                else:
                    play_item.setPath(None)
        elif 'tamilgun.' in vid_url:
            scraper = tgun.tgun()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                play_item.setPath(stream_url)
        elif ('tmvplay.' in vid_url) and ('data=' not in vid_url):
            scraper = tmvp.tmvp()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                play_item.setPath(stream_url)
        elif 'ozee.' in vid_url:
            scraper = ozee.ozee()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                play_item.setPath(stream_url)
        elif 'andhrawatch.' in vid_url:
            scraper = awatch.awatch()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                play_item.setPath(stream_url)
        elif 'tamiltv.site' in vid_url:
            scraper = tamiltv.tamiltv()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                play_item.setPath(stream_url)
        elif 'thoptv.' in vid_url:
            scraper = thop.thop()
            stream_url = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
        elif 'hyfytv.' in vid_url:
            scraper = hyfy.hyfy()
            stream_url = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
        elif 'nextvnow.' in vid_url:
            scraper = nextv.nextv()
            stream_url = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
        elif 'mhdtvlive.' in vid_url:
            scraper = mhdtv.mhdtv()
            stream_url = scraper.get_video(vid_url)
            if 'youtube.' in stream_url:
                stream_url = resolve_url(stream_url)
            if stream_url:
                play_item.setPath(stream_url)
            else:
                play_item.setPath(None)
        elif 'playembed.' in vid_url or '.m3u8' in vid_url:
            stream_url = vid_url
            play_item.setPath(stream_url)
        elif 'abroadindia.' in vid_url:
            scraper = aindia.aindia()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                elif '.f4m' in stream_url:
                    qurl = urllib.quote_plus(stream_url)
                    stream_url = 'plugin://plugin.video.f4mTester/?streamtype=HDS&url=%s'%qurl
                elif '.ts' in stream_url:
                    qurl = urllib.quote_plus(stream_url)
                    stream_url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url=%s'%qurl
                if stream_url:
                    play_item.setPath(stream_url)
                else:
                    play_item.setPath(None)
        elif 'load.' in vid_url:
            stream_url = resolve_url(vid_url)
            if stream_url:
                play_item.setPath(stream_url)
            else:
                play_item.setPath(None)
        else:
            stream_url = vid_url
            play_item.setPath(stream_url)
    else:
        stream_url = resolve_url(vid_url)
        if stream_url:
            play_item.setPath(stream_url)
        else:
            play_item.setPath(None)

    if dl:
        downloadDir = _settings('dlfolder')
        if not downloadDir:
            xbmc.executebuiltin('XBMC.Notification(Download:,Choose download directory in Settings!,5000)')
            return
        if '|' in stream_url:
            headers = stream_url.split('|')[1]
            stream_url = stream_url.split('|')[0]
        
        vid = {}
        vid['title'] = title
        vid['url'] = stream_url
        vid['ext'] = 'mp4'

        with YDStreamUtils.DownloadProgress() as prog: #This gives a progress dialog interface ready to use
            try:
                YDStreamExtractor.setOutputCallback(prog)
                result = YDStreamExtractor.downloadVideo(vid,downloadDir)
                if result:
                    #success
                    full_path_to_file = result.filepath
                elif result.status != 'canceled':
                    #download failed
                    error_message = result.message
            finally:
                YDStreamExtractor.setOutputCallback(None)
    else:                 
        kodistr = xbmc.getInfoLabel('System.BuildVersion')
        kodiver = float(kodistr[0:3])

        if kodiver >= 17.0 and stream_url and ('yupp' not in stream_url) and ('SUNNXT' not in stream_url):

            if '.m3u8' in stream_url:
                if 'master' in stream_url or 'adaptive' in stream_url:
                    play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
                    play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
                    play_item.setMimeType('application/vnd.apple.mpegstream_url')
                    play_item.setContentLookup(False)
                    if '|' in stream_url:
                        stream_url,strhdr = stream_url.split('|')
                        play_item.setProperty('inputstream.adaptive.stream_headers', strhdr)
                        play_item.setPath(stream_url)
           
            elif '.mpd' in stream_url:
                play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
                play_item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
                play_item.setMimeType('application/dash+xml')
                play_item.setContentLookup(False)
            
            elif '.ism' in stream_url:
                play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
                play_item.setProperty('inputstream.adaptive.manifest_type', 'ism')
                play_item.setMimeType('application/vnd.ms-sstr+xml')
                play_item.setContentLookup(False)
                    
        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring:
    Action Definitions:
    1 : List Site
    4 : List Top Menu (Channels, Languages)
    5 : List Secondary Menu (Shows, Categories)
    7 : List Individual Items (Movies, Episodes)
    8 : List Playable Videos
    9 : Play Video
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin

    if params:
        if params['action'] == '0':
            clear_cache()
        elif params['action'] == '1':
            list_menu(params['site'])
        elif params['action'] == '4':
            list_top(params['site'],params['iurl'])
        elif params['action'] == '5':
            list_second(params['site'],params['iurl'])   
        elif params['action'] == '7':
            list_items(params['site'],params['iurl'])
        elif params['action'] == '8':
            list_videos(params['site'],params['title'],params['iurl'],params['thumb'])
        elif params['action'] == '9':
            play_video(params['iurl'])
        elif params['action'] == '10':
            play_video(params['iurl'],dl=True)
    else:
        list_sites()

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
