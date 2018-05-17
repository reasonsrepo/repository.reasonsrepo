"""
    WatchOnlineMovies Kodi Addon
    Copyright (C) 2018 Milo

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
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re, requests, urllib, json
import jsunpack
import resolveurl
import HTMLParser


# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])
_addon = xbmcaddon.Addon()
_addonname = _addon.getAddonInfo('name')
_icon = _addon.getAddonInfo('icon')
_fanart = _addon.getAddonInfo('fanart')
mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}

def GetSearchQuery(sitename):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Search ' + sitename)
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_text = keyboard.getText()

    return search_text

def get_vidhost(url):
    """
    Trim the url to get the video hoster
    :return vidhost
    """
    parts = url.split('/')[2].split('.')
    vidhost = '%s.%s'%(parts[len(parts)-2],parts[len(parts)-1])
    return vidhost

def resolve_media(url,videos,title=''):
    non_str_list = [
        'olangal.',
        '#',
        'magnet:',
        'desihome.',
        'thiruttuvcd',
        'cineview',
        'bollyheaven',
        'videolinkz',
        'moviefk.co',
        'goo.gl',
        'imdb.',
        'mgid.',
        'atemda.',
        'movierulz.',
        'facebook.',
        'm2pub',
        'abcmalayalam',
        'india4movie.co',
        '.filmlinks4u',
        'tamilraja.',
        'multiup.',
        'filesupload.',
        'fileorbs.',
        'tamil.ws',
        'insurance-donate.',
        '.blogspot.',
        'yodesi.net',
        'desi-tashan.',
        'yomasti.co/ads',
        'ads.yodesi',
        '/ads/',
        'mylifeads.',
        ]

    embed_list = [
        'cineview',
        'bollyheaven',
        'videolinkz',
        'vidzcode',
        'embedzone',
        'embedsr',
        'fullmovie-hd',
        'links4.pw',
        'embedscr',
        'embedrip',
        'movembed',
        'power4link.us',
        'watchmoviesonline4u',
        'nobuffer.info',
        'yomasti.co',
        'techking.me',
        'onlinemoviesworld.xyz',
        'cinebix.com',
        'desihome.',
        'loan-forex.',
        'filmshowonline.',
        'vids.xyz',
        'business-tv.me',
        'telly-news.',
        'tellytimes.',
        'techking.',
        'adly.biz',
        'business-',
        'businessvoip.',
        'toptencar.',
        'loanadvisor.',
        'tellyfy.',
        ]

    if 'filmshowonline.net/media/' in url:
        try:
            r = requests.get(url, headers=mozhdr)
            clink = r.text
            cookies = r.cookies
            eurl = re.findall("var height.*?url: '(.*?)'", clink,
                              re.DOTALL)[0]
            enonce = re.findall("var height.*?nonce.*?'(.*?)'", clink,
                                re.DOTALL)[0]
            evid = re.findall("var height.*?link_id: ([^\s]*)", clink,
                              re.DOTALL)[0]
            values = {
                'echo': 'true',
                'nonce': enonce,
                'width': '848',
                'height': '480',
                'link_id': evid,
                }
            headers = mozhdr
            headers['Referer'] = url
            headers['X-Requested-With'] = 'XMLHttpRequest'
            emurl = requests.post(eurl, data=values, headers=headers,
                                  cookies=cookies).text
            strurl = re.findall('(http[^"]*)', emurl)[0].replace('\\',
                    '')
            if resolveurl.HostedMediaFile(strurl):
                vidhost = get_vidhost(strurl)
                if not title == '':
                    vidhost += ' | %s' % title
                videos.append((vidhost, strurl))
        except:
            pass
    elif 'justmoviesonline.com' in url:

        html = requests.get(url, headers=mozhdr).text
        src = re.search("atob\('(.*?)'", html)
        if src:
            src = src.group(1)
            try:
                strurl = re.findall('file":"(.*?)"', src.decode('base64'
                                    ))[0]
                vidhost = 'GVideo'
                strurl = urllib.quote_plus(strurl)
                videos.append((vidhost, strurl))
            except:
                pass
            try:
                strurl = re.findall('''source src=["'](.*?)['"]''',
                                    src.decode('base64'))[0]
                vidhost = get_vidhost(strurl)
                videos.append((vidhost, strurl))
            except:
                pass
        elif '?id=' in url:
            src = eval(re.findall('Loading.+?var.+?=([^;]+)', html,
                       re.DOTALL)[0])
            for item in src:
                if 'http' in item and 'justmovies' not in item:
                    strurl = item
            strurl += url.split('?id=')[1]
            strurl += '.mp4|User-Agent=%s' % mozhdr['User-Agent']
            vidhost = 'GVideo'
            strurl = urllib.quote_plus(strurl)
            videos.append((vidhost, strurl))
    elif 'videohost.site' in url or 'videohost1.com' in url:

        try:
            html = requests.get(url, headers=mozhdr).text
            pdata = eval(re.findall('Run\((.*?)\)',
                         html)[0]).decode('base64')
            linkcode = jsunpack.unpack(pdata).replace('\\', '')
            sources = json.loads(re.findall('sources:(.*?\}\])',
                                 linkcode)[0])
            for source in sources:
                strurl = source['file'] + '|Referer=%s' % url
                vidhost = get_vidhost(url) + ' | GVideo | %s' \
                    % source['label']
                strurl = urllib.quote_plus(strurl)
                videos.append((vidhost, strurl))
        except:
            pass
    elif 'videohost2.com' in url:

        html = requests.get(url, headers=mozhdr).text

        try:
            pdata = eval(re.findall('Loading video.+?(\[.+?\]);', html,
                         re.DOTALL)[0])
            if 'id=' in url:
                strurl = pdata[7] + url.split('=')[1] + pdata[9]
            else:
                strurl = pdata[7]
            vidhost = get_vidhost(url) + ' | GVideo'
            strurl = urllib.quote_plus(strurl + '|Referer=%s' % url)
            videos.append((vidhost, strurl))
        except:
            pass

        try:
            pdata = re.findall("atob\('([^']+)",
                               html)[0].decode('base64')
            strurl = re.findall("source\ssrc='([^']+)", pdata)[0] \
                + '|Referer=%s' % url
            vidhost = get_vidhost(url)
            strurl = urllib.quote_plus(strurl)
            videos.append((vidhost, strurl))
        except:
            pass
    elif 'tamildbox' in url:

        link = requests.get(url, headers=mozhdr).text
        try:
            mlink = SoupStrainer('div', {'id': 'player-embed'})
            dclass = BeautifulSoup(link, parseOnlyThese=mlink)
            if 'unescape' in str(dclass):
                etext = re.findall("unescape.'[^']*", str(dclass))[0]
                etext = urllib.unquote(etext)
                dclass = BeautifulSoup(etext)
            glink = dclass.iframe.get('src')
            if resolveurl.HostedMediaFile(glink):
                vidhost = get_vidhost(glink)
                videos.append((vidhost, glink))
        except:
            pass

        try:
            mlink = SoupStrainer('div',
                                 {'class': re.compile('^item-content')})
            dclass = BeautifulSoup(link, parseOnlyThese=mlink)
            glink = dclass.p.iframe.get('src')
            if resolveurl.HostedMediaFile(glink):
                vidhost = get_vidhost(glink)
                videos.append((vidhost, glink))
        except:
            pass

        try:
            if 'p,a,c,k,e,d' in link:
                linkcode = jsunpack.unpack(link).replace('\\', '')
                glink = re.findall("file\s*:\s*'(.*?)'", linkcode)[0]
            if 'youtu.be' in glink:
                glink = 'https://docs.google.com/vt?id=' + glink[16:]
            if resolveurl.HostedMediaFile(glink):
                vidhost = get_vidhost(glink)
                videos.append((vidhost, glink))
        except:
            pass

        try:
            codes = re.findall('"return loadEP.([^,]*),(\d*)', link)
            for (ep_id, server_id) in codes:
                burl = \
                    'http://www.tamildbox.com/actions.php?case=loadEP&ep_id=%s&server_id=%s' \
                    % (ep_id, server_id)
                bhtml = requests.get(burl, headers=mozhdr).text
                blink = re.findall('(?i)iframe\s*src="(.*?)"', bhtml)[0]
                vidhost = get_vidhost(blink)
                if 'googleapis' in blink:
                    blink = 'https://drive.google.com/open?id=' \
                        + re.findall('docid=([^&]*)', blink)[0]
                    vidhost = 'GVideo'
                videos.append((vidhost, blink))
        except:
            pass
    elif any([x in url for x in embed_list]):

        clink = requests.get(url, headers=mozhdr).text
        csoup = BeautifulSoup(clink)
        try:
            links = re.findall('''(?i)<iframe.+?src=["']([^'"]+)''',
                               clink)
            for strurl in links:

                    # xbmc.log('-------> Scraped link : %s' % strurl, xbmc.LOGNOTICE)

                if not any([x in strurl for x in non_str_list]):

                        # xbmc.log('-------> sending to resolveurl for checking : %s' % strurl, xbmc.LOGNOTICE)

                    if resolveurl.HostedMediaFile(strurl):
                        vidhost = get_vidhost(strurl)
                        if not title == '':
                            vidhost += ' | %s' % title
                        videos.append((vidhost, strurl))
                    else:
                        xbmc.log('-------> resolveurl cannot resolve : %s'
                                  % strurl, xbmc.LOGNOTICE)
        except:
            pass

        try:
            plink = csoup.find('a', {'class': 'main-button dlbutton'})
            strurl = plink.get('href')
            if not any([x in strurl for x in non_str_list]):
                if resolveurl.HostedMediaFile(strurl):
                    vidhost = get_vidhost(strurl)
                    if not title == '':
                        vidhost += ' | %s' % title
                    videos.append((vidhost, strurl))
        except:
            pass

        try:
            plink = csoup.find('div', {'class': 'aio-pulse'})
            strurl = plink.find('a')['href']
            if not any([x in strurl for x in non_str_list]):
                if resolveurl.HostedMediaFile(strurl):
                    vidhost = get_vidhost(strurl)
                    if not title == '':
                        vidhost += ' | %s' % title
                    videos.append((vidhost, strurl))
        except:
            pass

        try:
            plink = csoup.find('div',
                               {'class': re.compile('entry-content')})
            strurl = plink.find('a')['href']
            if not any([x in strurl for x in non_str_list]):
                if resolveurl.HostedMediaFile(strurl):
                    vidhost = get_vidhost(strurl)
                    if not title == '':
                        vidhost += ' | %s' % title
                    videos.append((vidhost, strurl))
        except:
            pass

        try:
            for linksSection in csoup.findAll('embed'):
                strurl = linksSection.get('src')
                if not any([x in strurl for x in non_str_list]):
                    if resolveurl.HostedMediaFile(strurl):
                        vidhost = get_vidhost(strurl)
                        if not title == '':
                            vidhost += ' | %s' % title
                        videos.append((vidhost, strurl))
        except:
            pass
    elif not any([x in url for x in non_str_list]):

        if resolveurl.HostedMediaFile(url):
            vidhost = get_vidhost(url)
            if not title == '':
                vidhost += ' | %s' % title
            videos.append((vidhost, url))
        else:
            xbmc.log('-------> resolveurl cannot resolve : %s' % url,
                     xbmc.LOGNOTICE)

    return


def get_categories():
    """
    Get the list of categories.
    :return: list
    """
    bu = 'https://movierulz.pe'
    r = requests.get(bu, headers=mozhdr)
    if r.url != bu:
        bu = r.url
    items = {}
    cats = re.findall('	<li id="menu-item-.*?" .*?"><a title="Bollywood Movie .*?" href="(.*?)">(.*?)<\/a><\/li>',r.text)
    # cats = re.findall('class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-[^4]*? href="((?=.*category).*?)">((?![^a-zA-Z]).*?)<',r.text) more ui items
    sno = 1
    for cat in cats:
        items[str(sno)+cat[1]] = cat[0]
        sno+=1
    items[str(sno)+'[COLOR blue]Hollywood Movie 2017[/COLOR]'] = bu + '/category/hollywood-movie-2017/'
    items[str(sno)+'[COLOR blue]Hollywood Movie 2016[/COLOR]'] = bu + '/category/hollywood-movie-2016/'
    items[str(sno)+'[COLOR blue]Hollywood Movie 2018[/COLOR]'] = bu + '/category/hollywood-movie-2018/'
    # items[str(sno)+'[COLOR blue]Comedy Movies[/COLOR]'] = bu + 'category/indian-movies/funny-movies/'
    # items[str(sno)+'[COLOR blue]Romantic Movies[/COLOR]'] = bu + 'category/romantic-movies/'
    items[str(sno)+'[COLOR yellow]** Search **[/COLOR]'] = bu + '/?s='
    
    return items

def get_movies(iurl):
    h = HTMLParser.HTMLParser()
    """
    Get the list of movies.
    :return: list
    """
    movies = []
    
    if iurl[-3:] == '?s=':
        search_text = GetSearchQuery('Movie Rulz')
        search_text = urllib.quote_plus(search_text)
        iurl += search_text

    html = requests.get(iurl, headers=mozhdr).text
    mlink = SoupStrainer('div', {'id':'container'})
    mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
    plink = SoupStrainer('nav', {'id':'posts-nav'})
    Paginator = BeautifulSoup(html, parseOnlyThese=plink)
    items = mdiv.findAll('div', {'class':'boxed film'})

    for item in items:
        title = h.unescape(item.text)
        url = item.find('a')['href']
        try:
            thumb = item.find('img')['src'].strip()
        except:
            thumb = _icon
        movies.append((title, thumb, url))
    
    if 'Older' in str(Paginator):
        nextli = Paginator.find('div', {'class':'nav-older'})
        purl = nextli.find('a')['href']
        pages = purl.split('/')
        currpg = int(pages[len(pages)-2]) - 1
        title = 'Next Page.. (Currently in Page %s)' % (currpg)
        movies.append((title, thumb, purl))
   
    return movies


def get_videos(url):
    """
    Get the list of videos.
    :return: list
    """
    videos = []
    if 'cinebix.com' in url:
        resolve_media(url,videos)
        return videos
        
    html = requests.get(url, headers=mozhdr).text
    mlink = SoupStrainer('div', {'class':'entry-content'})
    videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
    try:
        links = videoclass.findAll('a')
        for link in links:
            url = link.get('href')
            resolve_media(url,videos)
    except:
        pass

    mlink = SoupStrainer('div', {'class':'entry-content'})
    videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
    try:
        links = videoclass.findAll('a')
        for link in links:
            url = link.get('href')
            resolve_media(url,videos)
    except:
        pass

    try:
        url = videoclass.a.get('href')
        resolve_media(url,videos)
    except:
        pass    
    
    try:
        sources = json.loads(re.findall('vdf-data-json">(.*?)<',html)[0])
        url = 'https://www.youtube.com/watch?v=%s'%sources['videos'][0]['youtubeID']
        resolve_media(url,videos)
    except:
        pass
        
    return videos



def list_categories():
    """
    Create the list of categories in the Kodi interface.
    """
    categories = get_categories()
    listing = []
    for title,iurl in sorted(categories.iteritems()):
        list_item = xbmcgui.ListItem(label=title[1:])
        list_item.setArt({'thumb': _icon,
                          'icon': _icon,
                          'fanart': _fanart})
        url = '{0}?action=list_category&category={1}'.format(_url, urllib.quote(iurl))
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)


def list_movies(category):
    """
    Create the list of movies in the Kodi interface.
    """
    movies = get_movies(category)
    listing = []
    for movie in movies:
        list_item = xbmcgui.ListItem(label=movie[0])
        list_item.setArt({'thumb': movie[1],
                          'icon': movie[1],
                          'fanart': movie[1]})
        list_item.setInfo('video', {'title': movie[0]})
        if 'Next Page' in movie[0]:
            url = '{0}?action=list_category&category={1}'.format(_url, movie[2])
        else:
            url = '{0}?action=list_movie&thumb={1}&movie={2}'.format(_url, movie[1], movie[2])
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)
 
   
def list_videos(movie,thumb):
    """
    Create the list of playable videos in the Kodi interface.

    :param category: str
    """

    videos = get_videos(movie)
    listing = []
    for video in videos:
        list_item = xbmcgui.ListItem(label=video[0])
        list_item.setArt({'thumb': thumb,
                          'icon': thumb,
                          'fanart': thumb})
        list_item.setInfo('video', {'title': video[0]})
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=play&video={1}'.format(_url, video[1])
        is_folder = False
        listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)

def resolve_url(url):
    duration=7500   
    try:
        stream_url = resolveurl.HostedMediaFile(url=url).resolve()
        # If resolveurl returns false then the video url was not resolved.
        if not stream_url or not isinstance(stream_url, basestring):
            try: msg = stream_url.msg
            except: msg = url
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('URL Resolver',msg, duration, _icon))
            return False
    except Exception as e:
        try: msg = str(e)
        except: msg = url
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%('URL Resolver',msg, duration, _icon))
        return False
        
    return stream_url


def play_video(path):
    """
    Play a video by the provided path.

    :param path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    vid_url = play_item.getfilename()
    if 'WatchOnlineMovies' not in vid_url:
        stream_url = resolve_url(vid_url)
        if stream_url:
            play_item.setPath(stream_url)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring:
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin

    if params:
        if params['action'] == 'list_category':
            list_movies(params['category'])
        elif params['action'] == 'list_movie':
            list_videos(params['movie'],params['thumb'])
        elif params['action'] == 'play':
            play_video(params['video'])
    else:
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
