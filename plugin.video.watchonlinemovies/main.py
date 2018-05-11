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
import urlresolver

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

def resolve_media(url,videos):

    vidhost = get_vidhost(url)
    videos.append((vidhost,url))

    return

def get_categories():
    """
    Get the list of categories.
    :return: list
    """
    bu = 'http://www.watchonlinemovies.com.pk'
    r = requests.get(bu, headers=mozhdr)
    if r.url != bu:
        bu = r.url
    items = {}
    cats = re.findall('class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-has-children menu-item[^4]*?"><a href="((?=.*category).*?)">((?![^a-zA-Z]).*?)<',r.text)
    # cats = re.findall('class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-[^4]*? href="((?=.*category).*?)">((?![^a-zA-Z]).*?)<',r.text) more ui items
    sno = 1
    for cat in cats:
        items[str(sno)+cat[1]] = cat[0]
        sno+=1
    items[str(sno)+'[COLOR blue]2018 Hindi Movies[/COLOR]'] = bu + 'category/indian-movies/2018-full-movies/'
    items[str(sno)+'[COLOR blue]Comedy Movies[/COLOR]'] = bu + 'category/indian-movies/funny-movies/'
    items[str(sno)+'[COLOR blue]Romantic Movies[/COLOR]'] = bu + 'category/romantic-movies/'
    items[str(sno)+'[COLOR yellow]** Search **[/COLOR]'] = bu + '/?s='
    
    return items

def get_movies(iurl):
    """
    Get the list of movies.
    :return: list
    """
    movies = []
    
    if iurl[-3:] == '?s=':
        search_text = GetSearchQuery('WatchOnlineMovies')
        search_text = urllib.quote_plus(search_text)
        iurl += search_text

    html = requests.get(iurl, headers=mozhdr).text
    mlink = SoupStrainer('div', {'class':re.compile('postbox')})
    items = BeautifulSoup(html, parseOnlyThese=mlink)
    plink = SoupStrainer('div', {'class':'wp-pagenavi'})
    Paginator = BeautifulSoup(html, parseOnlyThese=plink)

    for item in items:
        title = item.h2.text
        url = item.h2.find('a')['href']
        try:
            thumb = item.find('img')['src'].strip()
        except:
            thumb = _icon
        movies.append((title, thumb, url))
    
    if 'next' in str(Paginator):
        nextli = Paginator.find('a', {'class':re.compile('page larger')})
        purl = nextli.get('href')
        if 'http' not in purl:
            purl = self.bu[:-12] + purl
        currpg = Paginator.find('span', {'class':re.compile('current')}).text
        pages = Paginator.findAll('a', {'class':re.compile('^page')})
        lastpg = pages[len(pages)-1].text
        title = 'Next Page.. (Currently in Page %s of %s)' % (currpg,lastpg)
        movies.append((title, _icon, purl))
   
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
    mlink = SoupStrainer('div', {'class':re.compile('^singcont')})
    videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
    try:
        links = videoclass.findAll('iframe')
        for link in links:
            url = link.get('src')
            resolve_media(url,videos)
    except:
        pass

    mlink = SoupStrainer('div', {'class':'entry-excerpt'})
    videoclass = BeautifulSoup(html, parseOnlyThese=mlink)
    try:
        links = videoclass.findAll('iframe')
        for link in links:
            if 'http' in str(link):
                url = link.get('src')
                resolve_media(url,videos)
    except:
        pass

    try:
        url = videoclass.p.a.get('href')
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
        stream_url = urlresolver.HostedMediaFile(url=url).resolve()
        # If urlresolver returns false then the video url was not resolved.
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
