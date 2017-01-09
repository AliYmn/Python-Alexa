from bs4 import BeautifulSoup
import urllib.request

"""
Author : Ali Yaman - aliymn.db@gmail.com
"""

class AlexaInfo():
    def __init__(self,url)->str:
        """str url bilgisi alır (constructor)"""
        self.url = url
        soup = BeautifulSoup(urllib.request.urlopen("http://www.alexa.com/siteinfo/{}".format(self.url)),'html.parser')
        self.soup = soup

    def alexaInfo(self):
        """Dünya, ülke, çıkma oranı, backlink gibi genel alexa bilgileri vermektedir."""
        global_rank, country_rank, bounce_rate, views, views_hours, search_engine, backlink = "0","0","0","0","0","0","0"
        # Rankları filitre ettik.
        ranks = self.soup.find_all('strong', attrs={'class': 'metrics-data align-vmiddle'})
        country_name = self.soup.find_all('span', attrs={'class': 'countryRank'})[0].find("h4").find("a").text
        global_rank = ranks[0].text.strip() # Dünya Rankı
        country_rank = ranks[1].text.strip()# Ülke rankı
        bounce_rate = ranks[2].text.strip() # Çıkma Oranı
        views = ranks[3].text.strip() # Günlük ziyaretçi başına düşen, görüntülenme sayısı
        views_hours = ranks[4].text.strip() # Sitedeki günlük saat görüntülenme sayısı
        if(len(ranks) == 5):
            ranks.insert(4,"")
        search_engine = ranks[5].text.strip() # Aramaların % kaçı arama motorundan gerçekleşiyor?
        backlink = self.soup.find_all('span',attrs={"class":'font-4 box1-r'})[0].text
        info_list = ["Global Rank", "Name of country", "Rank in Country ", "Bounce Rate", "Daily Pageviews per Visitor",
                     "Daily Time on Site", "Search Traffic", "Backlink"]
        result = [global_rank,country_name,country_rank,bounce_rate,views,views_hours,search_engine,backlink]
        list_to_dict = dict(zip(result,info_list))

        return list_to_dict

    def alaxaKeywords(self):
        """5 popüler kelime ve oranı bilgileri verir."""
        keywords_name = []
        keywords_value = []
        # Keywords filitre ettik.
        keywords = self.soup.find_all('table', attrs={'id': 'keywords_top_keywords_table'})[0].find_all('span',attrs={"class":""})
        for i in keywords:
            #Dict oluşturabilmek için, iki ayrı liste kayıt ediyoruz.
            if(keywords.index(i) % 2):
                keywords_name.append(i.text)
            else:
                keywords_value.append((i.text))

        list_to_dict = dict(zip(keywords_name,keywords_value))

        return list_to_dict

    def upstreamSites(self):
        """5 adet popüler ziyaretçi alınan siteden ismi ve oranını verir."""
        site_name = []
        site_value = []
        ups_site = self.soup.find_all('table', attrs={'id': 'keywords_upstream_site_table'})[0].find_all("a")
        ups_value = self.soup.find_all('table', attrs={'id': 'keywords_upstream_site_table'})[0].find_all('span',attrs={"class":""})

        for i in ups_value:
            site_value.append(i.text)

        for k in ups_site:
            site_name.append(k.text)

        list_to_dict = dict(zip(site_value,site_name))

        return list_to_dict
    def alexaRival(self):
        """Ortak ziyaretçiye sahip 5 adet site bilgisi verir. Rakip sitelerde diyebiliriz."""
        site_name = []
        rival_site = self.soup.find_all('table', attrs={'id': 'audience_overlap_table'})[0].find_all("a")
        for i in rival_site:
            site_name.append(i.text)

        return tuple(site_name)

    def subDomain(self):
        """Sub Domainler üzerinden aldığınız trafik yüzdesini gösterir."""
        site_name = []
        site_value = []

        sub_name = self.soup.find_all('table', attrs={'id': 'subdomain_table'})[0].find_all("span",attrs={"class":"word-wrap"})
        sub_value = self.soup.find_all('table', attrs={'id': 'subdomain_table'})[0].find_all('span',attrs={"class":""})

        for i in sub_name:
            site_name.append(i.text)

        for k in sub_value:
             site_value.append(k.text)

        list_to_dict = dict(zip(site_value, site_name))

        return list_to_dict
