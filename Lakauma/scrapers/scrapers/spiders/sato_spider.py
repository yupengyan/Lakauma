# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapers.items import VuokraKohdeItem
from ftfy import fix_text


#Spider hakemaan asuntokohteiden tietoa sato.fi sivulta. 
#TODO: muokkaa hakemaan kaikki tiedot
class SatoSpider(BaseSpider):
   name = "sato"
   allowed_domains = ["sato.fi"]
   start_urls = ["http://sato.fi/cps/sato/hs.xsl/-/html/hakutulos_vuokra.htm?cityname=&dd_city=259&dd_district=&dd_rooms1=1&dd_rooms2=1&dd_rooms3=1&dd_rooms4=1&dd_rooms5=1&dd_areafrom=0&dd_areato=99999&dd_rentfrom=0&dd_rentto=99999&dd_results=10"]

   def parse(self, response):
       hxs = HtmlXPathSelector(response)
       sitesOsoite = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 4) and parent::*)][normalize-space()]')
       sitesVuokra = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 6) and parent::*)]')
       sitesNeliot = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 5) and parent::*)]')
       sitesTyyppi = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]//a')
       sites = zip(sitesOsoite, sitesVuokra, sitesNeliot, sitesTyyppi)
       items = []
       for site in sites:
           item = VuokraKohdeItem()
           item['osoite'] = site[0].select('text()[normalize-space()]').extract()
           vajaa = str(site[1].select('text()[normalize-space()]').extract()).split(" ")
           parempi = vajaa[0].split("\'") 
           item['vuokra'] = parempi[1] + " e/kk"
           item['neliot'] = site[2].select('text()[normalize-space()]').extract()
           item['tyyppi'] = site[3].select('text()[normalize-space()]').extract()
           items.append(item)
       return items

