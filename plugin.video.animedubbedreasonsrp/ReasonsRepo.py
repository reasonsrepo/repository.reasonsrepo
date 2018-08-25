import os,xbmc

addon_path = xbmc.translatePath(os.path.join('special://home/addons', 'repository.reasonsrepo'))
addonxml=xbmc.translatePath(os.path.join('special://home/addons', 'repository.reasonsrepo','addon.xml'))




WRITEME='''<?xml version="1.0" encoding="UTF-8"?>
<addon id="repository.reasonsrepo" name="[COLOR blue]Reasons[/COLOR] [COLOR yellow]Repository[/COLOR]" version="1.0.0" provider-name="Reasons">
    <extension point="xbmc.addon.repository" name="[COLOR blue]Reasons[/COLOR] [COLOR yellow]Repository[/COLOR]">
    <dir>
        <info compressed="false">https://github.com/tvaddonsco/tva-resolvers-repo/raw/master/addons.xml</info>
        <checksum>https://github.com/tvaddonsco/tva-resolvers-repo/raw/master/addons.xml.md5</checksum>
        <datadir zip="true">https://github.com/tvaddonsco/tva-resolvers-repo/raw/master/zips/</datadir>
    </dir>
        <info compressed="false">https://raw.githubusercontent.com/reasonsrepo/repository.reasonsrepo/master/zips/addons.xml</info>
        <checksum>https://raw.githubusercontent.com/reasonsrepo/repository.reasonsrepo/master/zips/addons.xml.md5</checksum>
        <datadir zip="true">https://raw.githubusercontent.com/reasonsrepo/repository.reasonsrepo/master/zips</datadir>
    </extension>
    <extension point="xbmc.addon.metadata">
        <summary>Official Reasons Repository</summary>
        <description>All new kodi addons</description>
        <platform>all</platform>
    </extension>
</addon>
'''





if os.path.exists(addon_path) == False:
        os.makedirs(addon_path)


     
if os.path.exists(addonxml) == False:

    f = open(addonxml, mode='w')
    f.write(WRITEME)
    f.close()

    xbmc.executebuiltin('UpdateLocalAddons') 
    xbmc.executebuiltin("UpdateAddonRepos")
