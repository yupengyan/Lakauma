# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapers.items import VuokraKohdeItem
from geocode import oma_geocode

#Spider hakemaan asuntokohteiden tietoa sato.fi sivulta. 
class SatoSpider(BaseSpider):
    name = "sato" #This is the name you use to call the spider from update script.
    allowed_domains = ["sato.fi"]
    start_urls = ["http://sato.fi/cps/sato/hs.xsl/-/html/hakutulos_vuokra.htm?cityname=&dd_city=259&dd_district=&dd_rooms1=1&dd_rooms2=1&dd_rooms3=1&dd_rooms4=1&dd_rooms5=1&dd_areafrom=0&dd_areato=99999&dd_rentfrom=0&dd_rentto=99999&dd_results=10"]
    tulosten_pituus_vanha = 0
    tulosten_pituus_uusi = 0


    def parse(self, response):
       hxs = HtmlXPathSelector(response)
       sitesOsoite = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 4) and parent::*)][normalize-space()]')
       sitesVuokra = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 6) and parent::*)]')
       sitesNeliot = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 5) and parent::*)]')
       sitesTyyppi = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]//a')
#       sitesLinkki = hxs.select('//table[@class="results_rent_own"]/tbody//tr/td')
       sites = zip(sitesOsoite, sitesVuokra, sitesNeliot, sitesTyyppi)
       items = selector_silmukka(sites)    
       self.tulosten_pituus_vanha = self.tulosten_pituus_vanha + len(items)
       self.tulosten_pituus_uusi = self.tulosten_pituus_uusi + len(items)
       indexi = 1
       request = Request("http://sato.fi/cps/sato/hs.xsl/-/html/hakutulos_vuokra.htm?dd_city=259&dd_district=0&dd_senior=&dd_livingform=2&dd_areafrom=0&dd_areato=99999&dd_rentfrom=0&dd_rentto=99999&dd_loantype=&dd_f1=&dd_f2=&dd_f3=&dd_no=&dd_rooms1=1&dd_rooms2=1&dd_rooms3=1&dd_rooms4=1&dd_rooms5=1&dd_page=%s&dd_results=30&huoneisto=&srt="% (str(indexi + 1)), callback=self.parse_2)
       request.meta['item'] = items
       request.meta['indexi'] = indexi + 1
       return request

    def parse_2(self,response):
       hxs = HtmlXPathSelector(response)
       notFoundAttempt = hxs.select('//span[@class="strong"]')
       if("Hakua vastaavia" in notFoundAttempt.select('text()').extract()[0]):
           return response.meta['item']
       sitesOsoite = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 4) and parent::*)][normalize-space()]')
       sitesVuokra = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 6) and parent::*)]')
       sitesNeliot = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 5) and parent::*)]')
       sitesTyyppi = hxs.select('//td[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]//a')
#       sitesLinkki = hxs.select('//table/tbody//tr[@class=*]/td')
       sites = zip(sitesOsoite, sitesVuokra, sitesNeliot, sitesTyyppi)
       taulu = selector_silmukka(sites) 
       indexi = response.meta['indexi']
       for each in response.meta['item']:
            taulu.append(each)
       items = taulu 
       self.tulosten_pituus_uusi = self.tulosten_pituus_uusi + len(items)
       if(self.tulosten_pituus_vanha == self.tulosten_pituus_uusi):
            return items
       print indexi
       request = Request("http://sato.fi/cps/sato/hs.xsl/-/html/hakutulos_vuokra.htm?dd_city=259&dd_district=0&dd_senior=&dd_livingform=2&dd_areafrom=0&dd_areato=99999&dd_rentfrom=0&dd_rentto=99999&dd_loantype=&dd_f1=&dd_f2=&dd_f3=&dd_no=&dd_rooms1=1&dd_rooms2=1&dd_rooms3=1&dd_rooms4=1&dd_rooms5=1&dd_page=%s&dd_results=30&huoneisto=&srt="% (str(indexi + 1)), callback=self.parse_2)
       request.meta['item'] = items
       request.meta['indexi'] = indexi + 1
       return request

def selector_silmukka(sites):
    items = []
    for site in sites:
        item = VuokraKohdeItem()
        osoite = str(site[0].select('text()[normalize-space()]').extract()).split("\'")
        item["osoite"] = osoite[1]
        print "eka"
        vajaa = str(site[1].select('text()[normalize-space()]').extract()).split(" ")
        parempi = vajaa[0].split("\'") 
        item["vuokra"] = str(parempi[1])
        print "eka"           
        neliot_vaihe1 = str(site[2].select('text()[normalize-space()]').extract()).split(" ")
        neliot_vaihe2 = neliot_vaihe1[0].split("\'")
        item["neliot"] = str(neliot_vaihe2[1].replace(',','.'))
        vajaa_tyyppi =  str(site[3].select('text()[normalize-space()]').extract()).split("\'")           
        item["tyyppi"] = vajaa_tyyppi[1]
        place, (lat, lng) = "lol", (1, 3)
        #oma_geocode(osoite[1] + "Jyväskylä")  
        item["tarjoaja"] = "SATO"
        item["lat"] = lat
        item["lng"] = lng
        items.append(item)           
    return items
           
