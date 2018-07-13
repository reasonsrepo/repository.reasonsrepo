# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, os, ReasonsRepo,xbmcaddon,base64
import urlresolver
from addon.common.addon import Addon
from metahandler import metahandlers


addon_id='plugin.video.reasonsrepotestaddon'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
ADDON      = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
ICON = ADDON.getAddonInfo('icon')
FANART = ADDON.getAddonInfo('fanart')
PATH = 'Reasons Repo Test Addon'
VERSION = ADDON.getAddonInfo('version')
ART = ADDON_PATH + "/resources/icons/"
BASEURL = 'https://gomomovies.online/'
genreicon = ADDON_PATH + "/resources/genres/"
metaset = selfAddon.getSetting('enable_meta')
enbdubbed = selfAddon.getSetting('enable-dubbed')
enbpunj = selfAddon.getSetting('enable-punjabi')
metaget = metahandlers.MetaData()


def Main_menu():
    addDir('[B][COLOR red]Please Uninstall me[/COLOR][/B]','000000',0,ICON,FANART,'')
    addDir('[B][COLOR white]Featured Movies[/COLOR][/B]',BASEURL,5,ICON,FANART,'')
    addDir('[B][COLOR white]All Movies[/COLOR][/B]',BASEURL + 'movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]Trending Movies[/COLOR][/B]',BASEURL + 'trending/?get=movies',5,ICON,FANART,'')
    addDir('[B][COLOR white]Top Rated[/COLOR][/B]',BASEURL + 'ratings/?get=movies',5,ICON,FANART,'')
    addDir('[B][COLOR white]Top Rated[/COLOR][/B]',BASEURL + 'ratings/?get=movies',5,ICON,FANART,'')
    addDir('[B][COLOR white]Genre[/COLOR][/B]','',3,ICON,FANART,'')
    addDir('[B][COLOR white]Year[/COLOR][/B]','',33,ICON,FANART,'')
    addDir('[B][COLOR white]Search[/COLOR][/B]','url',6,ICON,FANART,'')
    addDir('[B][COLOR red]Please Uninstall me[/COLOR][/B]','',0,ICON,FANART,'')
    setView('files', 'menu-view')




def uninstall(url):
    addDir('[B][COLOR red]Please Uninstall me[/COLOR][/B]','000000',0,ICON,FANART,'')
    addDir('[B][COLOR white]Featured Movies[/COLOR][/B]',BASEURL,5,ICON,FANART,'')
    addDir('[B][COLOR white]All Movies[/COLOR][/B]',BASEURL + 'movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]Trending Movies[/COLOR][/B]',BASEURL + 'trending/?get=movies',5,ICON,FANART,'')
    addDir('[B][COLOR white]Top Rated[/COLOR][/B]',BASEURL + 'ratings/?get=movies',5,ICON,FANART,'')
    addDir('[B][COLOR white]Top Rated[/COLOR][/B]',BASEURL + 'ratings/?get=movies',5,ICON,FANART,'')
    addDir('[B][COLOR white]Genre[/COLOR][/B]','',3,ICON,FANART,'')
    addDir('[B][COLOR white]Year[/COLOR][/B]','',33,ICON,FANART,'')
    addDir('[B][COLOR white]Search[/COLOR][/B]','url',6,ICON,FANART,'')
    addDir('[B][COLOR red]Please Uninstall me[/COLOR][/B]','',0,ICON,FANART,'')
    setView('files', 'menu-view')
    xbmc.executebuiltin("XBMC.Notification([COLOR red]DELETE ME[/COLOR],[COLOR cornflowerblue]I am just a testing addon so you should uninstall me[/COLOR] ,100000)")






def Get_Genres():
    OPEN = Open_Url(BASEURL + 'trending/')
    Regex2 = re.compile('<a href="https:\/\/gomomovies\.online\/genre(.+?)">(.+?)<\/a>',re.DOTALL).findall(OPEN)
    for url,name in Regex2:
            name = name.replace('&amp;','&')
            url = BASEURL + 'genre' + url
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,genreicon + name + '.png',FANART,'')
#     xbmcplugin.SORT_METHOD_TITLE
    setView('files', 'menu-view')
	

def Get_year():
    OPEN = Open_Url(BASEURL + 'trending/')
    Regex2 = re.compile('<a href="https:\/\/gomomovies\.online\/release\/(.+?)">(.+?)<\/a>',re.DOTALL).findall(OPEN)
    for url,name in Regex2:
            url = BASEURL + 'release' + url
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,ICON,FANART,'')
#     xbmcplugin.SORT_METHOD_TITLE
    setView('files', 'menu-view')



def Get_content(url):

    OPEN = Open_Url(url)
    if 'movie' in url:
        Regex = re.compile('<h3><a href=\"(.+?)\">(.+?)</a></h3><span>(.+?)</span>',re.DOTALL).findall(OPEN)
        Regex2 = re.compile('</span><a href=\"(.+?)\">(.+?)</a></h3><span>(.+?)</span>',re.DOTALL).findall(OPEN)

        for url,name,year in Regex:
                icon = ICON
                items = len(Regex)
                name1 = name.replace('&#8217;','').replace('&#8230;','…')
                name = name1 + ' (' + year + ')'
                if metaset=='true':
                        try:
                                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,items)
                        except:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
                else:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
        try:
            np = re.compile("</article></div><div class=\"pagination\"><span>(.+?)</span><a.+?href=\"(.+?)\"><i id='nextpagination'",re.DOTALL).findall(OPEN)
            for pages,url in np: 
                pages = pages.replace('</span><span class="current">1','')
                addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ' + ' [COLOR yellow]Currently in ' + pages + '[/COLOR]',url,5,ART + 'nextpage.jpg',FANART,'')
        except:
            np = re.compile("<span>(.+?)</span><a .+?class='arrow_pag' href=\"(.+?)\"><i id='nextpagination'",re.DOTALL).findall(OPEN)
            for pages,url in np: 
                addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ' + ' [COLOR yellow]Currently in ' + pages + '[/COLOR]',url,5,ART + 'nextpage.jpg',FANART,'')
        setView('movies', 'movie-view')
    else:
        Regex2 = re.compile('<article id=\"post.+?class=\"item movies\"><div class=\"poster\"><img src=\"(.+?)\".+?<a href=\"(.+?)\"><div .+?href=.+?>(.+?)</a></h3><span>(.+?)</span></div></article>',re.DOTALL).findall(OPEN)
        for icon,url,name,year in Regex2:
                items = len(Regex2)
                name1 = name.replace('&#8217;','').replace('&#8230;','…')
                name = name1 + ' (' + year + ')'
                if metaset=='true':
                        try:
                                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,items)
                        except:
                                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
                else:
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
        try:
            np = re.compile("</article></div><div class=\"pagination\"><span>(.+?)</span><a.+?href=\"(.+?)\"><i id='nextpagination'",re.DOTALL).findall(OPEN)
            for pages,url in np: 
                addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ' + ' [COLOR yellow]Currently in ' + pages + '[/COLOR]',url,5,ART + 'nextpage.jpg',FANART,'')
        except:
            np = re.compile("<span>(.+?)</span><a .+?class='arrow_pag' href=\"(.+?)\"><i id='nextpagination'",re.DOTALL).findall(OPEN)
            for pages,url in np: 
                addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ' + ' [COLOR yellow]Currently in ' + pages + '[/COLOR]',url,5,ART + 'nextpage.jpg',FANART,'')
        setView('movies', 'movie-view')
		
	

def get_search(url):
    
    OPEN = Open_Url(url)
    Regex2 = re.compile('<div class=\"thumbnail animation-2\"><a href=\"(.+?)\"><img src=\"(.+?)\" alt="(.+?)" \/><span class=',re.DOTALL).findall(OPEN)

    for url,icon,name in Regex2:
            items = len(Regex2)
            name1 = name.replace('&#8217;','').replace('&#8230;','…')
            name = name1
            if metaset=='true':
                    try:
                            addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,items)
                    except:
                            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
            else:
                    addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
    try:
        np = re.compile("</article></div><div class=\"pagination\"><span>(.+?)</span><a.+?href=\"(.+?)\"><i id='nextpagination'",re.DOTALL).findall(OPEN)
        for pages,url in np: 
            pages = pages.replace('</span><span class="current">1','')
            addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ' + ' [COLOR yellow]Currently in ' + pages + '[/COLOR]',url,5,ART + 'nextpage.jpg',FANART,'')
    except:
        np = re.compile("<span>(.+?)</span><a .+?class='arrow_pag' href=\"(.+?)\"><i id='nextpagination'",re.DOTALL).findall(OPEN)
        for pages,url in np: 
            addDir('[B][COLOR blue]Next Page >>>[/COLOR][/B] ' + ' [COLOR yellow]Currently in ' + pages + '[/COLOR]',url,5,ART + 'nextpage.jpg',FANART,'')
    setView('movies', 'movie-view')



def Get_links(name,url):
    OPEN = Open_Url(url)
    Regex = re.compile('style="text-align:center">(.+?)</td>.+?href="(.+?)"',re.DOTALL).findall(OPEN)
    for name2,url in Regex:
            if urlresolver.HostedMediaFile(url):
                    addDir('[B][COLOR white]%s[/COLOR][/B]' %name2,url,100,iconimage,FANART,name)
    xbmc.executebuiltin('Container.SetViewMode(50)')


def Search():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = BASEURL + '?s=' + search
                xbmc.log(url)
                get_search(url)
    

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
        match = re.compile('<iframe class=\"meta.+?\" src=\"(.+?)\" frameborder=\"0\"',re.DOTALL).findall(OPEN)

        for link in match:
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
elif mode == 33: Get_year()
elif mode == 5 : Get_content(url)
elif mode == 6 : Search()
elif mode == 10 : Get_links(name,url)
elif mode == 99 : PT(url)
elif mode == 100 : resolve(name,url,iconimage,description)
elif mode == 56 : get_search(url)
elif mode == 0 : uninstall(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
