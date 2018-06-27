# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, os, ReasonsRepo,xbmcaddon,base64
import urlresolver
from addon.common.addon import Addon
from metahandler import metahandlers
from BeautifulSoup import BeautifulSoup, SoupStrainer
import requests, json
import jsunpack
from urlparse import parse_qsl


addon_id='plugin.video.reasonsfmovies'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
ADDON      = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
ICON = ADDON.getAddonInfo('icon')
FANART = ADDON.getAddonInfo('fanart')
PATH = 'fMovies'
VERSION = ADDON.getAddonInfo('version')
ART = ADDON_PATH + "/resources/icons/"
genreicon = ADDON_PATH + "/resources/genres/"
BASEURL =  selfAddon.getSetting('base_url')
metaset = selfAddon.getSetting('enable_meta')
metaget = metahandlers.MetaData()


def Main_menu():
    addDir('[B][COLOR white]Latest Movies[/COLOR][/B]',BASEURL + 'latests/cinema-movies.html',5,ICON,FANART,'')
    addDir('[B][COLOR white]Latest TV Series[/COLOR][/B]',BASEURL + 'latest/tv-series.html',595,ICON,FANART,'')
    addDir('[B][COLOR white]All TV Shows[/COLOR][/B]',BASEURL + 'kind/tv-series.html',595,ICON,FANART,'')
    addDir('[B][COLOR white]Latest TV Episodes[/COLOR][/B]',BASEURL + 'latest/tv-series.html',565,ICON,FANART,'')
    addDir('[B][COLOR white]Top IMDB[/COLOR][/B]',BASEURL + 'imdb.html',69,ICON,FANART,'')
    addDir('[B][COLOR white]Genre[/COLOR][/B]','',3,ICON,FANART,'')
    addDir('[B][COLOR white]Country[/COLOR][/B]','',56,ICON,FANART,'')
    addDir('[B][COLOR white]Year[/COLOR][/B]','',63,ICON,FANART,'')
    addDir('[B][COLOR white]Search[/COLOR][/B]','url',6,ICON,FANART,'')
    addDir('[B][COLOR red]Disclaimer: This addon is still in development and has some bugs. In future updates I will fix them.[/COLOR][/B]','','',ICON,FANART,'')
    setView('files', 'menu-view')

def Get_Genres():
    OPEN = Open_Url(BASEURL)
    Regex2 = re.compile("<li><a href=\"/genre(.+?)\" class='ads-evt' title=\".+?\">(.+?)</a></li>",re.DOTALL).findall(OPEN)
    for url,name in Regex2:
            url = 'https://www6.fmovies.io/genre' + url
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,genreicon + name + '.png',FANART,'')
    setView('files', 'menu-view')
def Get_year():
    OPEN = Open_Url(BASEURL)
    Regex2 = re.compile("<li><a href=\"/released-(.+?)\" class='ads-evt' title=\".+?\">(.+?)</a></li>",re.DOTALL).findall(OPEN)
    for url,name in Regex2:
            url = 'https://www6.fmovies.io/released-' + url
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,genreicon + name + '.png',FANART,'')
    setView('files', 'menu-view')
def Get_country():
    OPEN = Open_Url(BASEURL)
    Regex2 = re.compile("<li><a href=\"/country(.+?)\" class='ads-evt' title=\".+?\">(.+?)</a></li>",re.DOTALL).findall(OPEN)
    for url,name in Regex2:
            url = 'https://www6.fmovies.io/country' + url
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,genreicon + name + '.png',FANART,'')
    setView('files', 'menu-view')
	
def Get_content(url):

    OPEN = Open_Url(url)
#     Regex = re.compile('role="main">(.+?)role="navigation" ',re.DOTALL).findall(OPEN)
#     Regex2 = re.compile("<a href=\"(.+?)\".+?>\n.+<img.+?src=\"(.+?)\">\n.+?<h3>(.+?)</h3>\n.+\n\n.+<div class=\"quanlity\">(.+?)</div>",re.DOTALL).findall(OPEN)
    mlink = SoupStrainer('figure')
    items = BeautifulSoup(OPEN, parseOnlyThese=mlink)
    plink = SoupStrainer('ul', {'class':'pagination'})
    Paginator = BeautifulSoup(OPEN, parseOnlyThese=plink)
    for item in items:
            items = len(item)
            name1 = item.h3.text
            name = name1
            url1 = item.find('a')['href']
            url = 'https://www6.fmovies.io' + url1
            icon1 = item.find('img')['src'].strip()
            icon = 'https:' + icon1
            if metaset=='true':
                if 'season' in url:
                        addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,23,icon,items)
                else:
                        try:
                                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,items)
                        except:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
            else:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
    if 'next' in str(Paginator):
        nextli = Paginator.find('a', {'data-page':re.compile('1')})

        purl = nextli.get('href')
        url = url + purl
        name = 'Next Page..'
        addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ',url,5,ART + 'nextpage.jpg',FANART,'')
    np = re.compile('<a href=\".+?page=(.+?)\" data-page=\"(.+?)\">.+?</a>',re.DOTALL).findall(OPEN)
    
    for url1,name in np:
            url = url + '/?page=' + url1
            print url
            xbmc.log(url)
            
            if 'page' in np:
                addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ',url,5,ART + 'nextpage.jpg',FANART,'')
    setView('movies', 'movie-view')



def Get_latestepisode(url):

    OPEN = Open_Url(url)
#     Regex = re.compile('role="main">(.+?)role="navigation" ',re.DOTALL).findall(OPEN)
#     Regex2 = re.compile("<a href=\"(.+?)\".+?>\n.+<img.+?src=\"(.+?)\">\n.+?<h3>(.+?)</h3>\n.+\n\n.+<div class=\"quanlity\">(.+?)</div>",re.DOTALL).findall(OPEN)
    mlink = SoupStrainer('figure')
    items = BeautifulSoup(OPEN, parseOnlyThese=mlink)
    plink = SoupStrainer('ul', {'class':'pagination'})
    Paginator = BeautifulSoup(OPEN, parseOnlyThese=plink)
    for item in items:
            items = len(item)
            name1 = item.h3.text
            name = name1.replace('(','').replace(')','')
            url1 = item.find('a')['href']
            url = 'https://www6.fmovies.io' + url1
            icon1 = item.find('img')['src'].strip()
            icon = 'https:' + icon1
            try:
                episode = item.div.div.text
            except:
                episode = ''
            if metaset=='true':
                try:
                        addDir2('[B][COLOR white]%s[/COLOR][/B]' %name + ' [COLOR yellow]episode ' + episode,url,100,icon,items)
                except:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
            else:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
    if 'next' in str(Paginator):
        nextli = Paginator.find('a', {'data-page':re.compile('1')})

        purl = nextli.get('href')
        url = url + purl
        name = 'Next Page..'
        addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ',url,5,ART + 'nextpage.jpg',FANART,'')
    np = re.compile('<a href=\".+?page=(.+?)\" data-page=\"(.+?)\">.+?</a>',re.DOTALL).findall(OPEN)
    
    for url1,name in np:
            url = url + '/?page=' + url1
            print url
            xbmc.log(url)
            
            if 'page' in np:
                addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ',url,5,ART + 'nextpage.jpg',FANART,'')
    setView('movies', 'movie-view')








def Get_imdb(url):

    OPEN = Open_Url(url)
#     Regex = re.compile('role="main">(.+?)role="navigation" ',re.DOTALL).findall(OPEN)
#     Regex2 = re.compile("<a href=\"(.+?)\".+?>\n.+<img.+?src=\"(.+?)\">\n.+?<h3>(.+?)</h3>\n.+\n\n.+<div class=\"quanlity\">(.+?)</div>",re.DOTALL).findall(OPEN)
    mlink = SoupStrainer('figure')
    items = BeautifulSoup(OPEN, parseOnlyThese=mlink)
    plink = SoupStrainer('ul', {'class':'pagination'})
    Paginator = BeautifulSoup(OPEN, parseOnlyThese=plink)
    for item in items:
            items = len(item)
            name1 = item.h3.text
            name = name1.replace('(','').replace(')','').replace('English Audio','[COLOR yellow]English Audio[/COLOR]')
            url1 = item.find('a')['href']
            url = 'https://www6.fmovies.io' + url1
            icon1 = item.find('img')['src'].strip()
            icon = 'https:' + icon1
            if metaset=='true':
                if 'season' in url:
                        addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,23,icon,items)
                else:
                        try:
                                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,items)
                        except:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
            else:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
    if 'next' in str(Paginator):
        nextli = Paginator.find('a', {'data-page':re.compile('1')})

        purl = nextli.get('href')
        url = url + purl
        name = 'Next Page..'
        addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ',url,5,ART + 'nextpage.jpg',FANART,'')
    np = re.compile('<a href=\".+?page=(.+?)\" data-page=\"(.+?)\">.+?</a>',re.DOTALL).findall(OPEN)
    
    for url1,name in np:
            url = url + '/?page=' + url1
            print url
            xbmc.log(url)
            
            if 'page' in np:
                addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ',url,5,ART + 'nextpage.jpg',FANART,'')
    setView('movies', 'movie-view')



def Get_tvseries(url):

    OPEN = Open_Url(url)
#     Regex = re.compile('role="main">(.+?)role="navigation" ',re.DOTALL).findall(OPEN)
#     Regex2 = re.compile("<a href=\"(.+?)\".+?>\n.+<img.+?src=\"(.+?)\">\n.+?<h3>(.+?)</h3>\n.+\n\n.+<div class=\"quanlity\">(.+?)</div>",re.DOTALL).findall(OPEN)
    mlink = SoupStrainer('figure')
    items = BeautifulSoup(OPEN, parseOnlyThese=mlink)
    plink = SoupStrainer('ul', {'class':'pagination'})
    Paginator = BeautifulSoup(OPEN, parseOnlyThese=plink)
    for item in items:
            items = len(item)
            name1 = item.find("div", {"class": "title"})
            name2 = re.compile('<div class=\"title\">(.+?)</div>',re.DOTALL).findall(str(name1))
            for name in name2:
                    name = name
            url1 = item.find('a')['href']
            url = 'https://www6.fmovies.io' + url1
            icon1 = item.find('img')['src'].strip()
            icon = 'https:' + icon1
            if metaset=='true':
                if 'season' not in url:
                        addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,items)
                else:
                        try:
                                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,23,icon,items)
                        except:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,23,icon,FANART,'')
            else:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,23,icon,FANART,'')
    if 'next' in str(Paginator):
        nextli = Paginator.find('a', {'data-page':re.compile('1')})

        purl = nextli.get('href')
        url = url + purl
        name = 'Next Page..'
        addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ',url,5,ART + 'nextpage.jpg',FANART,'')
    np = re.compile('<a href=\".+?page=(.+?)\" data-page=\"(.+?)\">.+?</a>',re.DOTALL).findall(OPEN)
    
    for url1,name in np:
            url = url + '/?page=' + url1
            print url
            xbmc.log(url)
            
            if 'page' in np:
                addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ',url,5,ART + 'nextpage.jpg',FANART,'')
    setView('movies', 'movie-view')

def Get_tvepisodes(url):

    OPEN = Open_Url(url)
#     Regex = re.compile('role="main">(.+?)role="navigation" ',re.DOTALL).findall(OPEN)
    Regex2 = re.compile("<a href=\"(.+?)\">\n.+?<span class=\"name\" title=\"(.+?)\">.+?<\/span>",re.DOTALL).findall(OPEN)
    mlink = SoupStrainer('ul')
    items = BeautifulSoup(OPEN, parseOnlyThese=mlink)
    for url,name in Regex2:
            url = 'https://www6.fmovies.io' + url
            xbmc.log(url)
            name = name
            icon = iconimage
            try:
                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,items)
            except:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
    setView('files', 'menu-view')

		
	
# def Get_links(name,url):
#     OPEN = Open_Url(url)
#     Regex = re.compile('style="text-align:center">(.+?)</td>.+?href="(.+?)"',re.DOTALL).findall(OPEN)
#     for name2,url in Regex:
#             if urlresolver.HostedMediaFile(url):
#                     addDir('[B][COLOR white]%s[/COLOR][/B]' %name2,url,100,iconimage,FANART,name)
#     xbmc.executebuiltin('Container.SetViewMode(50)')


def Search():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = BASEURL + 'search.html?keyword=' + search + '&submit=Search'
                Get_content(url)

########################################

def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def addDir(name,url,mode,iconimage,fanart,description):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={"Title": name,"Plot":description})
    liz.setProperty('fanart_image', fanart)
    if mode==100:
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    else:
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addDir2(name,url,mode,iconimage,itemcount):
        name = name.replace('[B][COLOR white]','').replace('[/COLOR][/B]','')
        splitName=name.partition('(')
        simplename=""
        simpleyear=""
        if len(splitName)>0:
            simplename=splitName[0]
            simpleyear=splitName[2].partition(')')
        if len(simpleyear)>0:
            simpleyear=simpleyear[0]
	    mg = eval(base64.b64decode('bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iMzZjMWM1OWYwNTI0YTYzZTc3MmI5MGMzNzc4ZmIwOTciKQ=='))
	    meta = mg.get_meta('movie', name=simplename ,year=simpleyear)
        if meta['cover_url']=='':
            try:
                meta['cover_url']=iconimage
            except:
                meta['cover_url']=iconimage
        name = '[B][COLOR white]' + name + '[/COLOR][/B]' 
        meta['title'] = name
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
        liz.setInfo( type="Video", infoLabels= meta )
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        if meta['trailer']:
                contextMenuItems.append(('Play Trailer', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'mode': 99, 'url':meta['trailer']})))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        if not meta['backdrop_url'] == '':
                liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image',FANART)
        if mode==100 or mode==101:
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False,totalItems=itemcount)
        else:
             ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True,totalItems=itemcount)
        return ok

def notification(title, message, icon):
        addon.show_small_popup( addon.get_name(), message.title(), 5000, icon)
        return
    

def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)
	if addon.get_setting('auto-view') == 'true':
		xbmc.executebuiltin("Container.SetViewMode(%s)" % addon.get_setting(viewType) )



def PT(url):
        addon.log('Play Trailer %s' % url)
        notification( addon.get_name(), 'fetching trailer', addon.get_icon())
        xbmc.executebuiltin("PlayMedia(%s)"%url)
    
def resolve(name,url,iconimage,description):
    hosts = []
    stream_url = []
    host = ''
    try:
        OPEN = Open_Url(url)
        match = re.compile('var link_server_.+? = \"(.+?)\";',re.DOTALL).findall(OPEN)
        match2 = re.compile("var link_server_.+? = \'(.+?)\';",re.DOTALL).findall(OPEN)
        match3 = re.compile('var link_server_f.+? = \"(.+?)&.+?\";',re.DOTALL).findall(OPEN)
        for link in match:
            if "http" not in link:
                    link = 'https:' + link
            if not 'wholecloud' in link:
                if not 'vidtodo' in link:
                    if  urlresolver.HostedMediaFile(link).valid_url():   
                        label = link.split('//')[1].replace('www.','')
                        label = label.split('/')[0].split('.')[0].title()
                        label = label.replace('Tvad','TheVideo')
                        host = '[B][COLOR white]%s[/COLOR][/B]' %label
                        hosts.append(host)
                        stream_url.append(link)
        for link in match2:
            if not 'wholecloud' in link:
                if not 'vidtodo' in link:
                    if  urlresolver.HostedMediaFile(link).valid_url():   
                        label = link.split('//')[1].replace('www.','')
                        label = label.split('/')[0].split('.')[0].title()
                        label = label.replace('Tvad','TheVideo')
                        host = '[B][COLOR white]%s[/COLOR][/B]' %label
                        hosts.append(host)
                        stream_url.append(link)
        for link in match3:
            link = 'https:' + link
            if not 'wholecloud' in link:
                if not 'vidtodo' in link:
                    if  urlresolver.HostedMediaFile(link).valid_url():   
                        label = link.split('//')[1].replace('www.','')
                        label = label.split('/')[0].split('.')[0].title()
                        label = label.replace('Tvad','TheVideo')
                        host = '[B][COLOR white]%s[/COLOR][/B]' %label
                        hosts.append(host)
                        stream_url.append(link)
        
        if len(match) >1:
                dialog = xbmcgui.Dialog()
                ret = dialog.select('Please Select Host',hosts)
                if ret == -1:
                    return
                elif ret > -1:
                        url = stream_url[ret]
        else:
            url = re.compile('style="text-align:center">.+?</td>.+?href="(.+?)"').findall(OPEN)[0]
    except:
        xbmc.executebuiltin("XBMC.Notification([COLOR cornflowerblue]Sorry[/COLOR],[COLOR cornflowerblue]No Links Available[/COLOR] ,5000)") 
    try:
       stream=urlresolver.resolve(url)
       liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
       liz.setInfo(type="Video", infoLabels={"Title": description})
       liz.setProperty("IsPlayable","true")
       liz.setPath(stream)
       xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    except:pass

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2: 
                params=sys.argv[2] 
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}    
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
params=get_params()
url=None
name=None
iconimage=None
mode=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
#########################################################
	
if mode == None: Main_menu()
elif mode == 3: Get_Genres()
elif mode == 56: Get_country()
elif mode == 5 : Get_content(url)
elif mode == 23 : Get_tvepisodes(url)
elif mode == 595 : Get_tvseries(url)
elif mode == 565 : Get_latestepisode(url)
elif mode == 63 : Get_year()
elif mode == 6 : Search()
elif mode == 69 : Get_imdb(url)
# elif mode == 10 : Get_links(name,url)
elif mode == 99 : PT(url)
elif mode == 100 : resolve(name,url,iconimage,description)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
