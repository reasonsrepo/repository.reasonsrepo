# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, os, ReasonsRepo,xbmcaddon,base64
import urlresolver
from urlparse import parse_qsl
from addon.common.addon import Addon
from metahandler import metahandlers
from BeautifulSoup import BeautifulSoup, SoupStrainer
import requests,json
import jsunpack





addon_id='plugin.video.watchonlinemovies-New'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
addon_name = selfAddon.getAddonInfo('name')
ADDON      = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo('path')
ICON = ADDON.getAddonInfo('icon')
FANART = ADDON.getAddonInfo('fanart')
PATH = 'WatchOnlineMovies-New'
VERSION = ADDON.getAddonInfo('version')
ART = ADDON_PATH + "/resources/icons/"
BASEURL = 'http://www.watchonlinemovies.com.pk/'
metaset = selfAddon.getSetting('enable_meta')
enbdubbed = selfAddon.getSetting('enable-dubbed')
enbpunj = selfAddon.getSetting('enable-punjabi')
metaget = metahandlers.MetaData()


def Main_menu():
    addDir('[B][COLOR white]Featured Movies[/COLOR][/B]',BASEURL,5,ICON,FANART,'')
    addDir('[B][COLOR white]Hollywood Movies[/COLOR][/B]',BASEURL + 'category/hollywood-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]Bollywood Movies[/COLOR][/B]',BASEURL + 'category/indian-movies',5,ICON,FANART,'')
    addDir('[B][COLOR white]Categories[/COLOR][/B]','',3,ICON,FANART,'')
    addDir('[B][COLOR white]Year[/COLOR][/B]','',33,ICON,FANART,'')
    addDir('[B][COLOR white]Search[/COLOR][/B]','url',6,ICON,FANART,'')
    setView('files', 'menu-view')

def Get_Genres():
    OPEN = Open_Url(BASEURL)
    Regex2 = re.compile('<li id="menu-item-.+?" class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-.+?"><a href="(.+?)">(.+?)</a></li><li id=\"menu-item-',re.DOTALL).findall(OPEN)
    for url,name in Regex2:
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,5,ICON,FANART,'')
#     xbmcplugin.SORT_METHOD_TITLE
    setView('files', 'menu-view')
	

def Get_year():
    addDir('[B][COLOR white]2019 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2019-full-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2018 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2018-full-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2017 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2017-full-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2016 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2016-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2015 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2015-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2014 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2014-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2013 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2013-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2012 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2012-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2011 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2011-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2010 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2010-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2009 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2009-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2008 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2008-movies-list/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2007 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2007-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2006 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2006-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2005 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2005-movies-list/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2004 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2004-movies-list/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2003 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2003-movies-list/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2002 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2002-movies/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2001 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2001-movies-list/',5,ICON,FANART,'')
    addDir('[B][COLOR white]2000 Movies[/COLOR][/B]','http://www.watchonlinemovies.com.pk/category/indian-movies/2000-movies-list/',5,ICON,FANART,'')
    setView('files', 'menu-view')



def Get_content(url):

    OPEN = Open_Url(url)
#     Regex = re.compile('role="main">(.+?)role="navigation" ',re.DOTALL).findall(OPEN)
#     Regex2 = re.compile("<a href=\"(.+?)\".+?>\n.+<img.+?src=\"(.+?)\">\n.+?<h3>(.+?)</h3>\n.+\n\n.+<div class=\"quanlity\">(.+?)</div>",re.DOTALL).findall(OPEN)

    mlink = SoupStrainer('div', {'class':re.compile('postbox')})
    items = BeautifulSoup(OPEN, parseOnlyThese=mlink)
    plink = SoupStrainer('div', {'class':'wp-pagenavi'})
    Paginator = BeautifulSoup(OPEN, parseOnlyThese=plink)
    for item in items:
        items = len(item)
        name1 = item.h2.text
        name = item.h2.text
        if 'Hindi' in name1:
                name2 = re.compile('(.+?)Hindi',re.DOTALL).findall(name1)
                name = name2[0]
                # for name in name2:
                #     name = name
                try:
                    name2 = ''.join(map(str, name2))
                    name = name2.replace("\u2019s","s")
                    
                except:
                    name3 = name2
                    name = name3
        elif 'Full' in name1:
            name2 = re.compile('(.+?)Full.+',re.DOTALL).findall(name1)
        #     for name in name2:
        #         name = name
        
            try:
                name2 = ''.join(map(str, name2))
                name = name2.replace("\u2019s","s")
                
            except:
                name = name2
        if type(name) is list:
                name2 = ''.join(map(str, name[0].encode('utf8')))
                name = name2.replace("\u2019s","s") 
        url1 = item.h2.find('a')['href'].strip()
        url = url1
        try:
            icon = item.find('img')['src'].strip()
        except:
            icon = ICON
        if metaset=='true':
            try:
                addDir2('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,items)
            except:
                addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
        else:
            addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,'')
    
    if 'next' in str(Paginator):
        nextli = Paginator.find('a', {'class':re.compile('page larger')})
        purl = nextli.get('href')
        pages = Paginator.findAll('span', {'class':re.compile('pages')})
        lastpg = pages[len(pages)-1].text
        title = '[B][COLOR blue]Next Page..[/COLOR][COLOR yellow] (Currently in %s)' % (lastpg) + '[/COLOR][/B]'
        xbmc.log(purl)
        addDir(title,purl,5,ART + 'nextpage.jpg',FANART,'')
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
                url = BASEURL + '/?s=' + search + '&submit=Search'
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
    u=sys.argv[0]+'?url='+urllib.quote_plus(url)+'&mode='+str(mode)+'&name='+urllib.quote_plus(name)+'&iconimage='+urllib.quote_plus(iconimage)+'&description='+urllib.quote_plus(description)
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
    matches = []
    host = ''
    try:
        OPEN = Open_Url(url).lower()
        match = re.compile('<iframe src=(.+?) scrolling=n',re.DOTALL).findall(OPEN)
        match2 = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(OPEN)
        match3 = re.compile('<iframe width=.*?src=(.+?) frameborder',re.DOTALL).findall(OPEN)
        for link in match:
            matches.append(link)
        for link in match2:
                matches.append(link)
        for link in match3:
                matches.append(link)
        for link in matches:
            if  urlresolver.HostedMediaFile(link).valid_url():   
                label = link.split('//')[1].replace('www.','')
                label = label.split('/')[0].split('.')[0].title()
                label = label.replace('Tvad','TheVideo')
                host = '[B][COLOR white]%s[/COLOR][/B]' %label
                hosts.append(host)
                stream_url.append(link)
        if len(matches) >1:
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
        
#########################################################
                # Just Printing stuff #
#########################################################
print(str(PATH)+': '+str(VERSION))
print("Mode: "+str(mode))
print("URL: "+str(url))
print("Name: "+str(name))
print("IconImage: "+str(iconimage))
#########################################################
	
if mode == None: Main_menu()
elif mode == 3: Get_Genres()
elif mode == 33: Get_year()
elif mode == 5 : Get_content(url)
elif mode == 6 : Search()
elif mode == 10 : Get_links(name,url)
elif mode == 99 : PT(url)
elif mode == 100 : resolve(name,url,iconimage,description)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
