"""
    WatchOnlineMovies Kodi Addon
    Copyright (C) 2018 Reasons

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
    items = {'ARecently Uploaded Movies': bu,
            'B2018 Movies': bu + 'category/indian-movies/2018-full-movies/',
            'C2018 English Movies': bu + 'category/hollywood-movies/2018-movies-hollywood/',
            'Y[COLOR yellow]** Search **[/COLOR]': bu + '?s=',
            'Z[COLOR red]Note: This addon is still in development, so please keep it updated [/COLOR]': 'book'}
    
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
        title1 = item.h2.text
        try:
            title2 = title1.replace("Full Movie", "")
        except:
            title2 = title1.replace("Watch Online", "")
        try:
            title3 = title2.replace("Watch Online Placeholdernt", "")
        except:
            title3 = title2.replace(".", "")
        try:
            title4 = title3.replace(".", "")
        except:
            title4 = title3.replace("Watch Online Placeholder","")
        try:
            title5 = title4.replace("Watch Online", "")
        except:
            title5 = title4.replace("Download","")
        try:
            title6 = title5.replace("Watch Onlin", "")
        except:
            title6 = title5.replace("Placeholder","")
        try:
            title7 = title6.replace("HD Pri", "")
        except:
            title7 = title6.replace("Placeholder","")
        try:
            title8 = title7.replace("  Watch On", "")
        except:
            title8 = title7.replace("Placeholder","")
        try:
            title9 = title8.replace("  Watch", "")
        except:
            title9 = title8.replace("Placeholder","")
        try:
            title10 = title9.replace("Free Down", "")
        except:
            title10 = title9.replace("Placeholder","")
        try:
            title11 = title10.replace("Free D", "")
        except:
            title11 = title10.replace("Placeholder","")
        try:
            title12 = title11.replace("Free", "")
        except:
            title12 = title11.replace("Placeholder","")
        try:
            title13 = title12.replace("   F", "")
        except:
            title13 = title12.replace("Placeholder","")
        try:
            title14 = title13.replace("   Fr", "")
        except:
            title14 = title13.replace("Placeholder","")
        try:
            title15 = title14.replace("   Fre", "")
        except:
            title15 = title14.replace("Placeholder","")
        try:
            title16 = title15.replace(" HD", "")
        except:
            title16 = title15.replace("Placeholder","")
        try:
            title17 = title16.replace("    H", "")
        except:
            title17 = title16.replace("Placeholder","")
        try:
            title18 = title17.replace("    HD P", "")
        except:
            title18 = title17.replace("Placeholder","")
        try:
            title19 = title18.replace("  re", "")
        except:
            title19 = title18.replace("Placeholder","")
        try:
            title120 = title19.replace("  r", "")
        except:
            title120 = title19.replace("Placeholder","")
        # Coloring Years
        try:
            title21 = title120.replace("(2018)", "[COLOR yellow](2018)[/COLOR]")
        except:
            title21 = title120.replace("Placeholder","")
        try:
            title22 = title21.replace("(2016)", "[COLOR lightsalmon](2016)[/COLOR]")
        except:
            title22 = title21.replace("Placeholder","")
        try:
            title23 = title22.replace("(2015)", "[COLOR lime](2016)[/COLOR]")
        except:
            title23 = title22.replace("Placeholder","")
        # Language
        try:
            title24 = title23.replace("Hindi", "[COLOR green]Hindi[/COLOR]")
        except:
            title24 = title23.replace("Placeholder","")
        try:
            title25 = title24.replace("Dubbed", "[COLOR cyan]Dubbed[/COLOR]")
        except:
            title25 = title24.replace("Placeholder","")

        # Continued
        try:
            title26 = title25.replace("   nt o", "")
        except:
            title26 = title25.replace("Placeholder","")
        try:
            title27 = title26.replace("   nt F", "")
        except:
            title27 = title26.replace("Placeholder","")
        try:
            title28 = title27.replace("   nt", "")
        except:
            title28 = title27.replace("Placeholder","")
        try:
            title = title28.replace("   Pr", "")
        except:
            title = title28.replace("Placeholder","")

        url = item.h2.find('a')['href']
        try:
            thumb = item.find('img')['src'].strip()
        except:
            thumb = _icon
        movies.append((title, thumb, url))
    
    if 'next' in str(Paginator):

        nextli = Paginator.find('a', {'class':re.compile('page larger')})

        purl = nextli.get('href')
        pages = Paginator.findAll('span', {'class':re.compile('pages')})
        lastpg = pages[len(pages)-1].text
        title = 'Next Page.. (Currently in %s)' % (lastpg)
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
