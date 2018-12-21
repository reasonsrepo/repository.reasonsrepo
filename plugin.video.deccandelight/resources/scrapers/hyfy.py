'''
hyfytv deccandelight plugin
Copyright (C) 2018 Gujal

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
from _base_ import Scraper
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib, re, requests, base64, random
from resources.lib import cfscrape
from resources.lib import cache
import HTMLParser
import xbmc

class hyfy(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'http://hyfytv.co.in/language/'
        self.icon = self.ipath + 'hyfy.png'
        self.qvalues = ['Low','Med','Default','Good','High']
        self.bvalues = ['250','400','600','800','1200']
        self.qual = self.qvalues[int(self.settings('thopqual'))]
        self.bitrate = self.bvalues[int(self.settings('thopqual'))]
        self.list = {'01Tamil TV': self.bu + 'tamil/',
                     '02Telugu TV': self.bu + 'telugu/',
                     '03Malayalam TV': self.bu + 'malayalam/',
                     '04Kannada TV': self.bu + 'kannada/',
                     '05Hindi TV': self.bu + 'hindi/',
                     '06English TV': self.bu + 'english/',
                     '07Urdu TV': self.bu + 'urdu/',
                     '08Marathi TV': self.bu + 'marathi/',
                     '09Punjabi TV': self.bu + 'punjabi/',
                     '10Gujarathi TV': self.bu + 'gujarathi/',
                     '11Bangla TV': self.bu + 'bengali/',
                     '12Odiya TV': self.bu + 'odiya/'}

    def get_cf(self):
        durl = self.bu[:-9] + 'wp-includes/js/comment-reply.min.js'
        cj = cfscrape.get_tokens(durl,user_agent=self.hdr['User-Agent'])[0]
        ckstr = '; '.join([str(x)+"="+str(y) for x,y in cj.items()])
        return (cj,ckstr)
        
    def get_menu(self):
        return (self.list,7,self.icon)
        
    def get_items(self,iurl):
        cj,ckstr = cache.get(self.get_cf, 2)
        channels = []
        h = HTMLParser.HTMLParser()
        mlink = SoupStrainer('div', {'class':'content'})
        plink = SoupStrainer('div', {'class':'resppages'})
        nextpg = True
        while nextpg:
            html = requests.get(iurl, headers=self.hdr, cookies=cj).text
            mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
            items = mdiv.findAll('article')
            for item in items:
                title = h.unescape(item.h3.text).encode('utf8')
                if '(' in title:
                    title = re.findall('(.+?)\s\(',title)[0]
                url = item.find('a')['href']
                thumb = item.find('img')['src']
                channels.append((title, thumb, url))
            Paginator = BeautifulSoup(html, parseOnlyThese=plink)
            if 'chevron-right' in str(Paginator):
                iurl = Paginator.findAll('a')[-1].get('href')
            else:
                nextpg = False
        return (sorted(channels),9) 

    def get_video(self,url):
        cj,ckstr = cache.get(self.get_cf, 2)
        html = requests.get(url, headers=self.hdr, cookies=cj).text
        stream_url = ''

        try:
            stream_url = re.findall("Clappr\.Player.+?source:\s*'([^']+)", html)[0]
        except:
            pass
        
        if stream_url == '':
            tlink = re.findall('<iframe.+?src=[\'"]([^\'"]+)', html)[0]
            if 'file=' in tlink:
                tlink = re.findall('file=(.*)',tlink)[0]

            if 'hyfytv.' in tlink:          
                       
                XX11XX00XX = [{"id": "1","cid": "8","name": "Aaj Tak","cname": "Aaj_Tak","flag": "JY"},
                              {"id": "2","cid": "11","name": "india today","cname": "India_Today","flag": "JY"},
                              {"id": "3","cid": "13","name": "svbc","cname": "Sri_Venkateshwar_Bhakti","flag": "JY"},
                              {"id": "4","cid": "15","name": "Zoom","cname": "ZOOM","flag": "JY"},
                              {"id": "5","cid": "40","name": "ABN","cname": "ABN_Andhra_Jyothi","flag": "JY"},
                              {"id": "6","cid": "61","name": "sakshi","cname": "Sakshi_tv","flag": "JY"},
                              {"id": "7","cid": "108","name": "Jaya tv","cname": "Jaya_TV_HD","flag": "JY"},
                              {"id": "8","cid": "111","name": "Studio_n","cname": "Studio_n","flag": "JY"},
                              {"id": "9","cid": "115","name": "tv5 telugu","cname": "TV_5_News","flag": "JY"},
                              {"id": "10","cid": "117","name": "ET Now","cname": "ET_Now","flag": "JY"},
                              {"id": "11","cid": "118","name": "times now","cname": "Times_NOW","flag": "JY"},
                              {"id": "12","cid": "144","name": "Asianet News","cname": "Asianet_News","flag": "JY"},
                              {"id": "13","cid": "162","name": "Jeevan","cname": "Jeevan_TV","flag": "JY"},
                              {"id": "14","cid": "165","name": "Jaya Max","cname": "Jaya_Max","flag": "JY"},
                              {"id": "15","cid": "167","name": "Jaya Plus","cname": "Jaya_Plus","flag": "JY"},
                              {"id": "16","cid": "169","name": "Jaya Movie","cname": "Jaya_Movie","flag": "Y"},
                              {"id": "17","cid": "194","name": "maha news","cname": "Maha_News","flag": "JY"},
                              {"id": "18","cid": "198","name": "T news","cname": "T_News","flag": "JY"},
                              {"id": "19","cid": "203","name": "ndtv","cname": "NDTV_24x7","flag": "JY"},
                              {"id": "20","cid": "204","name": "ndtv profit","cname": "NDTV_Profit","flag": "JY"},
                              {"id": "21","cid": "205","name": "ndtv good times","cname": "NDTV_Good_Times","flag": "JY"},
                              {"id": "22","cid": "214","name": "Thanthi","cname": "Thanthi_TV","flag": "JY"},
                              {"id": "23","cid": "217","name": "People","cname": "Kairali_People_TV","flag": "JY"},
                              {"id": "24","cid": "227","name": "Vanitha","cname": "Vanitha","flag": "JY"},
                              {"id": "25","cid": "237","name": "News Time","cname": "News_Time_TV","flag": "JY"},
                              {"id": "26","cid": "238","name": "Ruposhi Bangla","cname": "Ruposhi_Bangla","flag": "Y"},
                              {"id": "27","cid": "249","name": "Amrita","cname": "Amrita_TV","flag": "JY"},
                              {"id": "28","cid": "262","name": "Kairali","cname": "Kairali_TV","flag": "JY"},
                              {"id": "29","cid": "263","name": "Kairali WE","cname": "Kairali_WE_TV","flag": "JY"},
                              {"id": "30","cid": "307","name": "Jaihind","cname": "Jaihind_tv","flag": "JY"},
                              {"id": "31","cid": "314","name": "Janasri","cname": "Janasri","flag": "Y"},
                              {"id": "32","cid": "374","name": "B4U Movies","cname": "B4U_Movies","flag": "JY"},
                              {"id": "33","cid": "446","name": "Seithigal","cname": "Seithigal","flag": "Y"},
                              {"id": "34","cid": "447","name": "v6 news","cname": "V6_News","flag": "JY"},
                              {"id": "35","cid": "599","name": "Sudharshan news","cname": "Sudarshan","flag": "JY"},
                              {"id": "36","cid": "637","name": "CVR News","cname": "CVR_News","flag": "JY"},
                              {"id": "37","cid": "695","name": "Sangeeth","cname": "Sangeet_Bangla","flag": "JY"},
                              {"id": "38","cid": "697","name": "Music India","cname": "Music_India","flag": "JY"},
                              {"id": "39","cid": "698","name": "OTV","cname": "OTV_Odisha_TV","flag": "JY"},
                              {"id": "40","cid": "699","name": "Tarang TV","cname": "Tarang_TV","flag": "JY"},
                              {"id": "41","cid": "700","name": "Tarang Music","cname": "Tarang_Music","flag": "JY"},
                              {"id": "42","cid": "701","name": "Prarthana tv","cname": "Prathana_TV","flag": "JY"},
                              {"id": "43","cid": "703","name": "Reporter","cname": "Reporter","flag": "Y"},
                              {"id": "44","cid": "704","name": "I News","cname": "I_News","flag": "JY"},
                              {"id": "45","cid": "705","name": "Shalom","cname": "Shalom","flag": "JY"},
                              {"id": "46","cid": "706","name": "Powervision","cname": "Powervision","flag": "Y"},
                              {"id": "47","cid": "717","name": "Athmeeyayathra","cname": "Athmeeyayathra","flag": "Y"},
                              {"id": "48","cid": "728","name": "Sankara","cname": "Sri_Sankara","flag": "JY"},
                              {"id": "49","cid": "778","name": "Divya tv","cname": "Divya_TV","flag": "JY"},
                              {"id": "50","cid": "807","name": "public tv","cname": "Public_TV","flag": "JY"},
                              {"id": "51","cid": "808","name": "9xm","cname": "9XM","flag": "JY"},
                              {"id": "52","cid": "809","name": "Kalaignar tv","cname": "Kalaignar_tv","flag": "Y"},
                              {"id": "53","cid": "810","name": "sirippoli","cname": "sirippoli","flag": "Y"},
                              {"id": "54","cid": "811","name": "chithiram tv","cname": "chithiram_tv","flag": "Y"},
                              {"id": "55","cid": "812","name": "Isai aruvi","cname": "Isai_aruvi","flag": "Y"},
                              {"id": "56","cid": "813","name": "Murasu","cname": "Murasu","flag": "Y"},
                              {"id": "57","cid": "879","name": "10 tv","cname": "10_TV","flag": "JY"},
                              {"id": "58","cid": "904","name": "Tollywood","cname": "Tollywood","flag": "Y"},
                              {"id": "59","cid": "984","name": "Captain","cname": "Captain_tv","flag": "JY"},
                              {"id": "60","cid": "985","name": "Captain News","cname": "Captain_News","flag": "JY"},
                              {"id": "61","cid": "1138","name": "cvr english news","cname": "CVR_English","flag": "JY"},
                              {"id": "62","cid": "1223","name": "Harvest tv","cname": "Harvest_tv","flag": "Y"},
                              {"id": "63","cid": "1247","name": "Puthiya Thalaimurai","cname": "Puthiya_Thalimurai","flag": "JY"},
                              {"id": "64","cid": "1309","name": "Mathrubhoomi","cname": "Mathrubhumi_News","flag": "JY"},
                              {"id": "65","cid": "1439","name": "Media oNe","cname": "Media_One_TV","flag": "JY"},
                              {"id": "66","cid": "1440","name": "Kaumudy tv","cname": "Kaumudy_TV","flag": "JY"},
                              {"id": "67","cid": "1441","name": "Goodness tv","cname": "Goodness_tv","flag": "Y"},
                              {"id": "68","cid": "1859","name": "Kerala Vision","cname": "Kerala_Vision","flag": "Y"},
                              {"id": "69","cid": "1932","name": "Manorama News","cname": "Manorama_News","flag": "JY"},
                              {"id": "70","cid": "1933","name": "Mazhavil","cname": "Mazhavil_Manorama","flag": "JY"},
                              {"id": "71","cid": "2165","name": "Tez","cname": "Tez","flag": "JY"},
                              {"id": "72","cid": "2248","name": "News7","cname": "News7_Tamil","flag": "JY"},
                              {"id": "73","cid": "2329","name": "Aastha Bhajan","cname": "Aastha_Bhajan","flag": "JY"},
                              {"id": "74","cid": "2437","name": "Flowers USA","cname": "Flowers_USA","flag": "Y"},
                              {"id": "75","cid": "2449","name": "al jazeera","cname": "AL_Jazeera","flag": "JY"},
                              {"id": "76","cid": "2595","name": "JUS Punjabi","cname": "JUS_Punjabi","flag": "Y"},
                              {"id": "77","cid": "2596","name": "JUS One","cname": "JUS_One","flag": "Y"},
                              {"id": "78","cid": "2597","name": "JUS 24x7","cname": "JUS_24x7","flag": "Y"},
                              {"id": "79","cid": "2615","name": "Russia Today","cname": "Russia_Today","flag": "Y"},
                              {"id": "80","cid": "2646","name": "Bharath today","cname": "Bharath_Today","flag": "Y"},
                              {"id": "81","cid": "2670","name": "T-Sat Nipuna","cname": "TSat_Nipuna","flag": "Y"},
                              {"id": "82","cid": "2714","name": "News24","cname": "News_24","flag": "JY"},
                              {"id": "83","cid": "2715","name": "E24","cname": "E_24","flag": "JY"},
                              {"id": "84","cid": "3021","name": "Vendhar","cname": "Vendhar_TV","flag": "JY"},
                              {"id": "85","cid": "3078","name": "Janam","cname": "Janam_TV","flag": "JY"},
                              {"id": "86","cid": "3145","name": "Vasanth","cname": "Vasanth_TV","flag": "JY"},
                              {"id": "87","cid": "3146","name": "Dheeran","cname": "Dheeran","flag": "Y"},
                              {"id": "88","cid": "3147","name": "Safari","cname": "Safari","flag": "Y"},
                              {"id": "89","cid": "3155","name": "Yupptv Classic Hindi","cname": "Yupptv_Classic_Hindi","flag": "Y"},
                              {"id": "90","cid": "3156","name": "Yupptv Premium","cname": "Yupptv_Premium","flag": "Y"},
                              {"id": "91","cid": "3157","name": "Yupp Malayalam","cname": "Yupp_Malayalam","flag": "Y"},
                              {"id": "92","cid": "3161","name": "Yupptv Classis Tamil","cname": "Yupptv_Classis_Tamil","flag": "Y"},
                              {"id": "93","cid": "3343","name": "Puthuyugam","cname": "Puthu_Yugam","flag": "JY"},
                              {"id": "94","cid": "3344","name": "Polimer","cname": "Polimer_TV","flag": "JY"},
                              {"id": "95","cid": "3345","name": "Polimer News","cname": "Polimer_News","flag": "JY"},
                              {"id": "96","cid": "3353","name": "Gyana Yogi","cname": "Gyana_Yogi","flag": "JY"},
                              {"id": "97","cid": "3354","name": "Darshana","cname": "Darshana","flag": "Y"},
                              {"id": "98","cid": "3483","name": "E5 telugu","cname": "E5_telugu","flag": "Y"},
                              {"id": "99","cid": "3527","name": "Suvarna News","cname": "Suvarna_News","flag": "JY"},
                              {"id": "100","cid": "3798","name": "NDTV","cname": "NDTV_India","flag": "JY"},
                              {"id": "101","cid": "3837","name": "Live today","cname": "Live_Today","flag": "JY"},
                              {"id": "102","cid": "3838","name": "ap24x7","cname": "ap24x7","flag": "Y"},
                              {"id": "103","cid": "3839","name": "Marian tv","cname": "Marian_tv","flag": "Y"},
                              {"id": "104","cid": "5027","name": "DW","cname": "dw","flag": "JY"},
                              {"id": "105","cid": "5029","name": "bbc","cname": "BBC_World_News","flag": "JY"},
                              {"id": "106","cid": "http://cnn_ibn_hls-lh.akamaihd.net/i/cnn_ibn_hls_n_1@174950/index_3_av-b.m3u8","name": "CNN IBN NEWS","cname": "CNN_NEWS_18","flag": "JK"},
                              {"id": "107","cid": "http://cdn7.live247stream.com/desibeats/tv/playlist.m3u8","name": "DESI BEATS","cname": "DESI_BEATS","flag": "K"},
                              {"id": "108","cid": "http://mediacontent-lh.akamaihd.net/i/marathiabpnew_1@188093/master.m3u8","name": "ABP_Majha","cname": "ABP_Majha","flag": "JK"},
                              {"id": "109","cid": "http://nicls1-lh.akamaihd.net/i/lst_1@26969/master.m3u8","name": "LSTV","cname": "Loksabha_TV","flag": "JK"},
                              {"id": "110","cid": "http://bcliveuniv-lh.akamaihd.net/i/iptv1_1@194050/master.m3u8","name": "CBN USA","cname": "CBN_USA","flag": "K"},
                              {"id": "111","cid": "https://mediauseast.akamaized.net/us/us1_live.m3u8","name": "Bloomberg","cname": "BLOOMBERG","flag": "K"},
                              {"id": "112","cid": "http://live.cloud6.in:1935/live1/ntvuae/playlist.m3u8","name": "NTV UAE","cname": "NTV_UAE","flag": "K"},
                              {"id": "113","cid": "http://etv_bihar_jharkh-lh.akamaihd.net/i/etv_bihar_hls_1@175736/index_1_av-b.m3u8","name": "ETV Bihar","cname": "ETV_BIHAR","flag": "JK"},
                              {"id": "114","cid": "http://etv_rajasthan_hl-lh.akamaihd.net/i/etv_rajasthan_hls_1@175738/index_1_av-b.m3u8","name": "ETV Rajasthan","cname": "ETV_RAJASTHAN","flag": "JK"},
                              {"id": "115","cid": "http://etv_up_hls-lh.akamaihd.net/i/etv_up_hls_1@175735/index_1_av-b.m3u8","name": "ETV UP","cname": "ETV_UP","flag": "JK"},
                              {"id": "116","cid": "http://etv_mp_hls-lh.akamaihd.net/i/etv_mp_hls_1@175737/index_3_av-b.m3u8","name": "ETV MP","cname": "ETV_MP","flag": "JK"},
                              {"id": "117","cid": "http://etvurdulive-lh.akamaihd.net/i/etv_urdu_live_1@373059/index_3_av-b.m3u8","name": "ETV Urdu","cname": "ETV_Urdu","flag": "JK"},
                              {"id": "118","cid": "http://367449830.r.cdnsun.net/367449830/_definst_/tv9tel/playlist.m3u8","name": "TV9 Telugu","cname": "TV9_Telugu_News","flag": "JK"},
                              {"id": "119","cid": "http://367449830.r.cdnsun.net/367449830/_definst_/sneha/playlist.m3u8","name": "TV1 Telugu","cname": "TV1","flag": "JK"},
                              {"id": "120","cid": "https://ind45-lh.akamaihd.net/i/ind45_starvijay@571066/master.m3u8","name": "vijay uk","cname": "VIJAY_TV_UK","flag": "YT"},
                              {"id": "121","cid": "https://ind29-lh.akamaihd.net/i/ind29_zeetamilus@562685/master.m3u8","name": "zee tamil us","cname": "ZEE_TAMIL_US","flag": "YT"},
                              {"id": "122","cid": "https://nwk2-lh.akamaihd.net/i/uk2_zeetamil@423327/master.m3u8","name": "zee tamil uk","cname": "ZEE_TAMIL_UK","flag": "YT"},
                              {"id": "123","cid": "https://nwk6-lh.akamaihd.net/i/us6_jayamaxus@334830/master.m3u8","name": "Jayamax us","cname": "JAYAMAX_US","flag": "YT"},
                              {"id": "124","cid": "https://hlsengent-lh.akamaihd.net/i/hls23_jayamaxuk9@174795/master.m3u8","name": "jayamax uk","cname": "JAYAMAX_UK","flag": "YT"},
                              {"id": "125","cid": "https://nwk6-lh.akamaihd.net/i/us6_jayamoviesus@334833/master.m3u8","name": "jmovies us","cname": "JAYAMOVIES_US","flag": "YT"},
                              {"id": "126","cid": "https://hlsengent-lh.akamaihd.net/i/hls23_jayamoviesuk10@174805/master.m3u8","name": "jayamovies uk","cname": "JAYAMOVIES_UK","flag": "YT"},
                              {"id": "127","cid": "https://nwk6-lh.akamaihd.net/i/us6_jayaus@82052/master.m3u8","name": "jayatv us","cname": "JAYA_TV_US","flag": "YT"},
                              {"id": "128","cid": "https://hlsengextra-lh.akamaihd.net/i/hls26_jayatvuk5@4914/master.m3u8","name": "jayatv uk","cname": "JAYA_TV_UK","flag": "YT"},
                              {"id": "129","cid": "https://nwk6-lh.akamaihd.net/i/us6_rajdigitalplusus@199573/master.m3u8","name": "raj digital plus us","cname": "RAJ_DIGITAL_PLUS_US","flag": "YT"},
                              {"id": "130","cid": "https://ind46-lh.akamaihd.net/i/ind46_kbo@573502/master.m3u8","name": "KBO HD","cname": "KBO_HD","flag": "YT"},
                              {"id": "131","cid": "https://ind46-lh.akamaihd.net/i/ind46_kbous@81919/master.m3u8","name": "KBO HD US","cname": "KBO_HD_US","flag": "YT"},
                              {"id": "132","cid": "https://ind14-lh.akamaihd.net/i/ind14_tet@82394/master.m3u8","name": "TET tv hdtamil","cname": "TET_TV_HD","flag": "YT"},
                              {"id": "133","cid": "https://us1-lh.akamaihd.net/i/us1_danmusic@307764/master.m3u8","name": "DAN Music","cname": "DAN_MUSIC","flag": "YT"},
                              {"id": "134","cid": "https://ind14-lh.akamaihd.net/i/ind14_tamilone@516618/master.m3u8","name": "Tamilone","cname": "TAMIL_ONE","flag": "YT"},
                              {"id": "135","cid": "https://hlsengextra-lh.akamaihd.net/i/hls24_rajtvuk8@4887/master.m3u8","name": "Rajtv uk","cname": "RAJTV_UK","flag": "YT"},
                              {"id": "136","cid": "https://nwk6-lh.akamaihd.net/i/us6_rajtvus@321198/master.m3u8","name": "rajtv us","cname": "RAJTV_US","flag": "YT"},
                              {"id": "137","cid": "https://hlsengextra-lh.akamaihd.net/i/hls24_rajdigitalpuk7@4886/master.m3u8","name": "rajdigitallus uk","cname": "RAJ_DIGITAL_PLUS_UK","flag": "YT"},
                              {"id": "138","cid": "https://us1-lh.akamaihd.net/i/us1_dantv@307763/master.m3u8","name": "dan tamil oli","cname": "DAN_TAMIL_OLI","flag": "YT"},
                              {"id": "139","cid": "http://158.69.124.9:1935/5aabtv/5aabtv/playlist.m3u8","name": "5aab tv","cname": "5AAB_TV","flag": "K"},
                              {"id": "140","cid": "http://start.agmediachandigarh.com/gaundapunjab/tv/playlist.m3u8","name": "Haunda Punjab","cname": "HAUNDA_PUNJAB","flag": "K"},
                              {"id": "141","cid": "http://104.237.59.106/live/Global_punjab.m3u8","name": "Global Punjab","cname": "GLOBAL_PUNJAB","flag": "K"},
                              {"id": "142","cid": "http://cdn13.live247stream.com/globalsanjh/tv/playlist.m3u8","name": "Global Sanjh","cname": "GLOBAL_SANJH","flag": "K"},
                              {"id": "143","cid": "http://stream-03.sg1.dailymotion.com/52/dm/3/x3m6nld/live-4.m3u8","name": "Fashiontv","cname": "FASHION_TV","flag": "K"},
                              {"id": "144","cid": "http://live.haappyapp.com:1935/ka-ayush/ayush-devotee/ayush-devotee/chunklist_w1776334619.m3u8","name": "Ayush tv","cname": "AYUSH_TV","flag": "K"},
                              {"id": "145","cid": "http://209.58.177.175/isirihls/isiri.m3u8","name": "Isiri TV","cname": "ISIRI_TV","flag": "K"},
                              {"id": "146","cid": "http://45.112.203.254:1935/live/live/live/chunklist_w1923026879.m3u8","name": "Namma TV","cname": "NAMMA_TV","flag": "K"},
                              {"id": "147","cid": "http://45.79.203.234:1935/murasutv/myStream/playlist.m3u8","name": "Malai Murasu","cname": "Malai_Murasu","flag": "JK"},
                              {"id": "148","cid": "http://45.79.203.234:1935/win/myStream/chunklist_w1164972194.m3u8","name": "Win TV","cname": "WIN_TV","flag": "K"},
                              {"id": "149","cid": "http://cdn.ibctamil.com/ibc-music/smil:ibcmusic.smil/playlist.m3u8","name": "IBC Isai","cname": "IBC_ISAI","flag": "K"},
                              {"id": "150","cid": "http://59299831b66d0.streamlock.net/ibc-comedy/smil:ibccomedy.smil/playlist.m3u8","name": "IBC Comedy","cname": "IBC_COMEDY","flag": "K"},
                              {"id": "151","cid": "https://stream.namadhutv.com/NamadhuLive/myStream/playlist.m3u8","name": "Namadhu TV","cname": "NAMADHU_TV","flag": "K"},
                              {"id": "152","cid": "http://209.58.160.22/Sanatvhls/live.m3u8","name": "Sana TV","cname": "SANA_TV","flag": "K"},
                              {"id": "153","cid": "http://supertvcloud.purplestream.in/supertvorg/ngrp:supertv_all/playlist.m3u8","name": "Super TV","cname": "SUPER_TV","flag": "K"},
                              {"id": "154","cid": "http://live.tamilvision.tv:8081/TVI/SD/playlist.m3u8","name": "TamilVision","cname": "TAMILVISION_TV","flag": "K"},
                              {"id": "155","cid": "http://live.streamjo.com:1935/eetlive/eettv/playlist.m3u8","name": "EET TV","cname": "EET_TV","flag": "K"},
                              {"id": "156","cid": "http://live.wmncdn.net/tamilan/live.stream/index.m3u8","name": "Tamilan TV","cname": "TAMILAN_TV","flag": "K"},
                              {"id": "157","cid": "http://live.wmncdn.net/peppers/live.stream/tracks-v1a1/index.m3u8","name": "Peppers TV","cname": "PEPPERS_TV","flag": "K"},
                              {"id": "158","cid": "http://livematrix.in:1935/live/sangamamtv/playlist.m3u8","name": "Sangamam TV","cname": "SANGAMAM_TV","flag": "K"},
                              {"id": "159","cid": "http://edge-ind.inapcdn.in:1935/wrap/smarts4n.stream_aac/playlist.m3u8","name": "Velicham TV","cname": "VELICHAM_TV","flag": "K"},
                              {"id": "160","cid": "http://nithya.live-s.cdn.bitgravity.com/cdn-live/_definst_/nithya/live/nithyanandatv500/playlist.m3u8","name": "Nithyananda TV","cname": "NITHYANANDA_TV","flag": "K"},
                              {"id": "161","cid": "http://live.streamjo.com:1935/cctv/live/playlist.m3u8","name": "Canada Tamils TV","cname": "CANADA_TAMIL_TV","flag": "K"},
                              {"id": "162","cid": "http://149.202.205.24:1935/DIGITAL/myStream/playlist.m3u8","name": "ARY Digital","cname": "ARY_DIGITAL","flag": "K"},
                              {"id": "163","cid": "http://cdn.live5.in:1935/live/shakthi/chunklist_w1967668811.m3u8","name": "Sakthi Cable TV","cname": "SAKTHI_CABLE_TV","flag": "K"},
                              {"id": "164","cid": "http://218.248.64.82:1935/live/spbala_webA.sdp/chunklist_w1896527840.m3u8","name": "SPB Music","cname": "SPB_MUSIC","flag": "K"},
                              {"id": "165","cid": "http://150.242.21.2/tamiltv.m3u8","name": "Tamil TV","cname": "TAMIL_TV","flag": "K"},
                              {"id": "166","cid": "http://45.79.203.234:1935/apple6/myStream/chunklist_w437053765.m3u8","name": "Apple UHD TV","cname": "APPLE_UHD_TV","flag": "K"},
                              {"id": "167","cid": "http://150.242.21.2/aaryaa.m3u8","name": "Aaryaa tv","cname": "AARYAA_TV","flag": "K"},
                              {"id": "168","cid": "http://livematrix.in:1935/live/maxtv/chunklist_w1965272757.m3u8","name": "Max tv","cname": "MAX_TV","flag": "K"},
                              {"id": "169","cid": "http://bosstv3.chennaistream.net/bosstv/mp4:bosstvlive/chunklist_w1825712831.m3u8","name": "Boss TV","cname": "BOSS_TV","flag": "K"},
                              {"id": "170","cid": "http://arratvcloud.purplestream.in/arratvorg/smil:arratv.smil/chunklist_b256000.m3u8","name": "Arra TV","cname": "ARRA_TV","flag": "K"},
                              {"id": "171","cid": "http://45.79.203.234:1935/deva/myStream/chunklist_w989871748.m3u8","name": "Deva TV","cname": "DEVA_TV","flag": "K"},
                              {"id": "172","cid": "http://rtmp.santhoratv.zecast.net/santhoratv/santhoratv/chunklist_w1469848631.m3u8","name": "Santhora tv","cname": "SANTHORA_TV","flag": "K"},
                              {"id": "173","cid": "http://stream.mslive.in:1935/1yes/gd416/chunklist_w1603773825.m3u8","name": "1YES","cname": "1YES_TV","flag": "K"},
                              {"id": "174","cid": "http://rtmp.santhoratv.zecast.net/tamilbusinesstv/tamilbusinesstv/chunklist_w1229072400.m3u8?nimblesessionid=30425576","name": "Tamil Business TV","cname": "TAMIL_BUSINESS_TV","flag": "K"},
                              {"id": "175","cid": "http://88.202.186.202:1935/cdn/deepamtvuk/playlist.m3u8","name": "Deepam TV","cname": "DEEPAM_TV","flag": "K"},
                              {"id": "176","cid": "http://akaram.zecast.net/akaram-live/akaramkidz/playlist.m3u8","name": "Akaram Kidz","cname": "AKARAM_KIDZ","flag": "K"},
                              {"id": "177","cid": "http://209.58.177.186/tamilvisiontvhls/tamilvisiontv.m3u8","name": "Tamil Vision","cname": "TAMIL_VISION","flag": "K"},
                              {"id": "178","cid": "http://ibn_lokmat_hls-lh.akamaihd.net/i/ibn_lokmat_hls_n_1@178974/index_3.m3u8","name": "IBN_Lokmat","cname": "IBN_Lokmat","flag": "JK"},
                              {"id": "179","cid": "http://newsx.live-s.cdn.bitgravity.com/cdn-live/_definst_/newsx/live/indianewsnational_384/playlist.m3u8","name": "India News","cname": "India_news","flag": "JK"},
                              {"id": "180","cid": "http://indiatvnews-lh.akamaihd.net/i/ITV_1@199237/master.m3u8","name": "India TV","cname": "India_TV","flag": "JK"},
                              {"id": "181","cid": "http://139.59.13.228:8081/live/stream/playlist.m3u8","name": "Kanak News","cname": "Kanak_TV","flag": "JK"},
                              {"id": "182","cid": "http://54.255.155.24:1935//Live/_definst_/amlst:sweetbcha1novD94L240P/playlist.m3u8","name": "Prathana","cname": "Prathana_TV","flag": "JK"},
                              {"id": "183","cid": "http://cdn-01.bonus-tv.ru:8080/1HDmusic/index.m3u8","name": "1HD Music","cname": "1HD_MUSIC","flag": "K"},
                              {"id": "184","cid": "http://live.wmncdn.net/bhaagya1/54f1d025e282fee369a8f2d44998dc49.sdp/mono.m3u8","name": "Bhaagya","cname": "BHAAGYA_TV","flag": "K"},
                              {"id": "185","cid": "http://live.wmncdn.net/vaani/4c6a67731a3b12a9c3cd50a2d67d06d0.sdp/mono.m3u8","name": "Vaani","cname": "VAANI_TV","flag": "K"},
                              {"id": "186","cid": "http://nicls3-lh.akamaihd.net/i/ddpunjabi_1@122402/master.m3u8","name": "DD Punjabi","cname": "DD_Punjabi","flag": "JK"},
                              {"id": "187","cid": "http://dmi.mangomolo.com:1935/dubaitv/smil:dubaitv.smil/playlist.m3u8","name": "Dubai TV","cname": "DUBAI_TV","flag": "K"},
                              {"id": "188","cid": "http://mahuaacloud.purplestream.in/mahuaaplus/mahuaaplus3-live.smil/playlist.m3u8","name": "Mahua Plus","cname": "Mahua_Plus","flag": "JK"}]

                chid = re.findall('=([^/]+)',tlink)[0]
                item_id = 1
                for item in XX11XX00XX:
                    if item['cname']==chid:
                        item_id = int(item['id'])
                        break

                cdata = XX11XX00XX[item_id-1]
                flag = cdata['flag']

                if flag == 'JY':
                    surl = 'http://hyfytv.co.in/juzplayall/%s.m3u8|User-Agent=%s&Cookie=%s'%(chid,self.hdr['User-Agent'],ckstr)
                    shtml = requests.get(surl, headers=self.hdr,cookies=cj).text
                    stream_url = re.findall('(http.+%s\.m3u8)'%self.bitrate,shtml)[0] + '|User-Agent=%s&Cookie=%s'%(self.hdr['User-Agent'],ckstr)
                elif flag == 'Y':
                    surl = 'https://origin-api-dhtv.dailyhunt.in/v2/item/yupptvredirect/%s/master.m3u8'%cdata['cid']
                    stream_url = requests.get(surl, headers=self.hdr, allow_redirects=False).headers['Location'] + '|User-Agent=%s'%self.dhdr['User-Agent']
                else:
                    xbmc.log('%s not resolvable.\n'%tlink,xbmc.LOGNOTICE)

            elif '.m3u8' in tlink:
                stream_url = tlink + '|User-Agent=%s'%self.hdr['User-Agent']
                
            else:
                xbmc.log('%s not resolvable.\n'%tlink,xbmc.LOGNOTICE)

                       
        return stream_url