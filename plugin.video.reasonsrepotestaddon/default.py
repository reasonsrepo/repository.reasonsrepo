# -*- coding: utf-8 -*-
import urllib2, urllib, xbmcgui, xbmcplugin, xbmc, re, sys, os, ReasonsRepo,xbmcaddon,base64
import urlresolver
from urlparse import parse_qsl
from addon.common.addon import Addon
from metahandler import metahandlers
from BeautifulSoup import BeautifulSoup, SoupStrainer
import requests,json
import jsunpack


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
BASEURL = 'https://ww5.dubbedanime.net/'
genreicon = ADDON_PATH + "/resources/genres/"
metaset = selfAddon.getSetting('enable_meta')
enbdubbed = selfAddon.getSetting('enable-dubbed')
metaget = metahandlers.MetaData()




def Main_menu():
    addDir('[B][COLOR red]Please Uninstall me[/COLOR][/B]','000000',0,ICON,FANART,'','','')
    addDir('[B][COLOR white]Latest Episodes[/COLOR][/B]',BASEURL,5,ICON,FANART,'','','')
    addDir('[B][COLOR white]Ongoing Anime[/COLOR][/B]',BASEURL + 'ongoing-anime',9,ICON,FANART,'','','')
    addDir('[B][COLOR white]Search[/COLOR][/B]','url',6,ICON,FANART,'','')
    addDir('[B][COLOR white]Random[/COLOR][/B]','url',3,ICON,FANART,'','')
    addDir('[B][COLOR red]Please Uninstall me[/COLOR][/B]','000000',0,ICON,FANART,'','','')
    setView('files', 'menu-view')

def uninstall(url):
    addDir('[B][COLOR red]Please Uninstall me[/COLOR][/B]','000000',0,ICON,FANART,'','','')
    addDir('[B][COLOR white]Latest Episodes[/COLOR][/B]',BASEURL,5,ICON,FANART,'','','')
    addDir('[B][COLOR white]Ongoing Anime[/COLOR][/B]',BASEURL + 'ongoing-anime',9,ICON,FANART,'','','')
    addDir('[B][COLOR white]Search[/COLOR][/B]','url',6,ICON,FANART,'','','')
    addDir('[B][COLOR red]Please Uninstall me[/COLOR][/B]','000000',0,ICON,FANART,'','','')
    setView('files', 'menu-view')
    xbmc.executebuiltin("XBMC.Notification([COLOR red]DELETE ME[/COLOR], [COLOR green] I am not ready yet so you should uninstall me [/COLOR] ,10000)")


def Get_Genres():
    OPEN = Open_Url(BASEURL)
    Regex2 = re.compile('<a class="nav-link" href="(.+?)">(.+?)<\/a>',re.DOTALL).findall(OPEN)
    for url,name in Regex2:
        xbmc.log(url + ' needs to work')
        name = name.encode('utf8')
        if 'http' not in url:
            url = url.replace('/','')
            url = BASEURL + url

        
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,25,ICON,FANART,'','','')
    xbmcplugin.SORT_METHOD_TITLE
    setView('files', 'menu-view')
	

def Get_year():

    setView('files', 'menu-view')



def Get_content(url):

    OPEN = Open_Url(url)
#     Regex = re.compile('role="main">(.+?)role="navigation" ',re.DOTALL).findall(OPEN)
#     Regex2 = re.compile("<a href=\"(.+?)\".+?>\n.+<img.+?src=\"(.+?)\">\n.+?<h3>(.+?)</h3>\n.+\n\n.+<div class=\"quanlity\">(.+?)</div>",re.DOTALL).findall(OPEN)

    mlink = SoupStrainer('figure', {'class':re.compile('fig-box text-left')})
    items = BeautifulSoup(OPEN, parseOnlyThese=mlink)
    for item in items:
        name1 = item.figcaption.text
        
        try:
            name2 = name1.replace('Movie','[COLOR yellow] Movie[/COLOR]').replace('Episode',' Episode')
        except:
            name2 = name1
        url1 = item.find('a')['href'].strip()
        url = url1
        
        if 'subbed' in url:
            name3 = name2 + ' [COLOR blue]SUBBED[/COLOR]'
        elif 'dubbed' in url:
            name3 = name2 + ' [COLOR limegreen]DUBBED[/COLOR]'

        name = name3.encode('utf8')

        description3 = item.p.text
        description = " [COLOR yellow]Posted: " + description3 + "[/COLOR]"
        try:
            icon1 = item.find('img')['src'].strip()
            icon = 'https:' + icon1
        except:
            icon = ICON

        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,description,'','')
    
    setView('movies', 'movie-view')
		

################################## Get Ongoing Shows ###################################

def Get_ongoing(url):

    OPEN = Open_Url(url)
#     Regex = re.compile('role="main">(.+?)role="navigation" ',re.DOTALL).findall(OPEN)
#     Regex2 = re.compile("<a href=\"(.+?)\".+?>\n.+<img.+?src=\"(.+?)\">\n.+?<h3>(.+?)</h3>\n.+\n\n.+<div class=\"quanlity\">(.+?)</div>",re.DOTALL).findall(OPEN)

    mlink = SoupStrainer('div', {'class':re.compile('pr-2 anime-img-cont position-relative')})
    items = BeautifulSoup(OPEN, parseOnlyThese=mlink)
    for item in items:
        name1 = item.a.text
        
        try:
            name2 = name1.replace('Movie','[COLOR yellow] Movie[/COLOR]').replace('Episode',' Episode')
        except:
            name2 = name1
        url1 = item.find('a')['href'].strip()
        url = url1
        
        name = name2.encode('utf8')
        try:
            icon = item.find('img')['src'].strip()
        except:
            icon = ICON

        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,25,icon,FANART,'','','')
    
    setView('movies', 'movie-view')


################################# Get Episodes ######################################################

def Get_episodes(url):

    OPEN = Open_Url(url)
#     Regex = re.compile('role="main">(.+?)role="navigation" ',re.DOTALL).findall(OPEN)
#     Regex2 = re.compile("<a href=\"(.+?)\".+?>\n.+<img.+?src=\"(.+?)\">\n.+?<h3>(.+?)</h3>\n.+\n\n.+<div class=\"quanlity\">(.+?)</div>",re.DOTALL).findall(OPEN)
    
    mlink = SoupStrainer('figure', {'class':re.compile('fig-box text-left')})
    mlink2 = SoupStrainer('div', {'class':re.compile('w-80 px-sm-2 px-0')})
    items = BeautifulSoup(OPEN, parseOnlyThese=mlink)
    descriptionparse = BeautifulSoup(OPEN, parseOnlyThese=mlink2)

    for item in items:
        name1 = item.figcaption.text
        
        try:
            name2 = name1.replace('Movie','[COLOR yellow] Movie[/COLOR]').replace('Episode',' Episode')
        except:
            name2 = name1
        url = item.find('a')['href'].strip()
        if 'subbed' in url:
            name3 = name2 + ' [COLOR blue]SUBBED[/COLOR]'
        elif 'dubbed' in url:
            name3 = name2 + ' [COLOR limegreen]DUBBED[/COLOR]'

        name = name3.encode('utf8')
        if 'Summary' in str(descriptionparse):
            description1 = descriptionparse.div.p.text
            description = description1.encode('utf8')
        else:
            description = ''

        tagline = re.compile('<p><b>Title:</b>(.+)</p><p><b>Engli').findall(OPEN)[0]
        rating = re.compile('<img src="(.+?)" width="100%" style="max-width:').findall(OPEN)[0]

        try:
            icon1 = item.find('img')['src'].strip()
            icon = 'https:' + icon1
        except:
            icon = ICON
        FANART = rating
        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,100,icon,FANART,description,tagline,rating)
    
    setView('movies', 'movie-view')


################################# Get Search ######################################################

def Get_search(url):

    OPEN = Open_Url(url)
#     Regex = re.compile('role="main">(.+?)role="navigation" ',re.DOTALL).findall(OPEN)
#     Regex2 = re.compile("<a href=\"(.+?)\".+?>\n.+<img.+?src=\"(.+?)\">\n.+?<h3>(.+?)</h3>\n.+\n\n.+<div class=\"quanlity\">(.+?)</div>",re.DOTALL).findall(OPEN)

    mlink = SoupStrainer('div', {'class':re.compile('w-50 d-inline-block pr-2')})
    items = BeautifulSoup(OPEN, parseOnlyThese=mlink)
    for item in items:
        name1 = item.a.text
        
        try:
            name2 = name1.replace('Movie','[COLOR yellow] Movie[/COLOR]').replace('Episode',' Episode')
        except:
            name2 = name1
        url1 = item.find('a')['href'].strip()
        url = url1
        

        name = name2.encode('utf8')
        try:
            icon1 = item.find('img')['src'].strip()
            icon = 'https:' + icon1
        except:
            icon = ICON

        addDir('[B][COLOR white]%s[/COLOR][/B]' %name,url,25,icon,FANART,'','','')
    
    setView('movies', 'movie-view')




def Get_links(name,url):
    OPEN = Open_Url(url)
    Regex = re.compile('style="text-align:center">(.+?)</td>.+?href="(.+?)"',re.DOTALL).findall(OPEN)
    for name2,url in Regex:
            if urlresolver.HostedMediaFile(url):
                    addDir('[B][COLOR white]%s[/COLOR][/B]' %name2,url,100,iconimage,FANART,name,'','')
    xbmc.executebuiltin('Container.SetViewMode(50)')


def Search():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = BASEURL + 'search?term=' + search
                Get_search(url)
    

########################################

def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def addDir(name,url,mode,iconimage,fanart,description,tagline,rating):
    u=sys.argv[0]+'?url='+urllib.quote_plus(url)+'&mode='+str(mode)+'&name='+urllib.quote_plus(name)+'&iconimage='+urllib.quote_plus(iconimage)+'&description='+urllib.quote_plus(description)+'&tagline='+urllib.quote_plus(tagline)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={"Title": name,"Tagline": tagline,"fanart_image": rating,"Plot":description})
    liz.setProperty("fanart_image", rating)
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
        match = re.compile('{"host":"mp4upload","id":"(.+?)","type":"(.+?)","date"',re.DOTALL).findall(OPEN)
        match2 = re.compile('{"host":"trollvid","id":"(.+?)","type":"(.+?)","date"',re.DOTALL).findall(OPEN)
        for link,lang in match:
            if 'subbed' in lang:
                vidhost = '[COLOR limegreen]' + lang + '[/COLOR]' 
            if 'dubbed' in lang:
                vidhost = '[COLOR yellow]' + lang + '[/COLOR]' 
            link = 'https://mp4upload.com/embed-' + link + '.html'
            if "http" not in link:
                    link = 'https:' + link
            if not 'wholecloud' in link:
                if not 'vidtodo' in link:
                    if  urlresolver.HostedMediaFile(link).valid_url():   
                        label = link.split('//')[1].replace('www.','')
                        label = label.split('/')[0].split('.')[0].title()
                        label = label.replace('Tvad','TheVideo')
                        host = '[B][COLOR white]%s[/COLOR][/B]' %label + ' ' + vidhost
                        hosts.append(host)
                        stream_url.append(link)
        for link,lang in match2:
            if 'subbed' in lang:
                vidhost = '[COLOR limegreen]' + lang + '[/COLOR]' 
            if 'dubbed' in lang:
                vidhost = '[COLOR yellow]' + lang + '[/COLOR]' 
            link = 'https://trollvid.net/embed/' + link
            if not 'wholecloud' in link:
                if not 'vidtodo' in link:
                    if  urlresolver.HostedMediaFile(link).valid_url():   
                        label = link.split('//')[1].replace('www.','')
                        label = label.split('/')[0].split('.')[0].title()
                        label = label.replace('Tvad','TheVideo')
                        host = '[B][COLOR white]%s[/COLOR][/B]' %label + ' ' + vidhost
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
            try : 
                url1 = re.compile('{"host":"trollvid","id":"(.+?)","type').findall(OPEN)[0]
                url = 'https://trollvid.net/embed/' + url1
            except:
                url1 = re.compile('{"host":"mp4upload","id":"(.+?)","type').findall(OPEN)[0]
                url = 'https://mp4upload.com/embed-' + url1 + '.html'
            
        
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
tagline=None
rating=None


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
try:        
        tagline=urllib.unquote_plus(params["tagline"])
except:
        pass
try:        
        rating=urllib.unquote_plus(params["rating"])
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
elif mode == 9 : Get_ongoing(url)
elif mode == 25 : Get_episodes(url)
elif mode == 0 : uninstall(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
