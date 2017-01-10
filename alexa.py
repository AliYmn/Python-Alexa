from bs4 import BeautifulSoup
import urllib.request

"Bu modül, Alexa.com üzerinden sitelerin analiz bilgilerine erişmenizi sağlar."

class AlexaInfo():
    """
    Alexa.com üzerinden, analiz bilgileri almanızı sağlayan sınıftır.

    # Arguments #
    url=str()   | String formatında, url bilgisi alır.

    # Properties #
    url=str()   | Alexa.com üzerinden taranacak siteyi, bu değişken üzerinden belirlenir.
    """

    def __init__(self,url=str()):
        """str url bilgisi alır (constructor)"""

        self.url = url # Site Url
        # taranan sitenin, html kodları
        soup = BeautifulSoup(urllib.request.urlopen("http://www.alexa.com/siteinfo/{}".format(self.url)),'html.parser')
        # Html kodlar
        self.soup = soup

    def alexaInfo(self) -> dict:
        """Dünya, ülke, çıkma oranı, backlink gibi genel alexa bilgileri vermektedir."""

        # Değişkenleri standart olarak "0" belirledik.
        global_rank, country_rank, bounce_rate, views, views_hours, search_engine, backlink = "0","0","0","0","0","0","0"

        #Rankları filitre edelim.
        ranks = self.soup.find_all('strong', attrs={'class': 'metrics-data align-vmiddle'})

        #Değişkenlere aktarma
        country_name = self.soup.find_all('span', attrs={'class': 'countryRank'})[0].find("h4").find("a").text
        global_rank = ranks[0].text.strip() # Dünya Rankı
        country_rank = ranks[1].text.strip()# Ülke rankı
        bounce_rate = ranks[2].text.strip() # Çıkma Oranı
        views = ranks[3].text.strip() # Günlük ziyaretçi başına düşen, görüntülenme sayısı
        views_hours = ranks[4].text.strip() # Sitedeki günlük saat görüntülenme sayısı

        # Search_engine kontrol, yeni siteler olmayabilir. Eğer yoksa "" boş değer atar.
        if(len(ranks) == 5):
            ranks.insert(4,"")

        #Aranma Hacmi
        search_engine = ranks[5].text.strip() # Aramaların % kaçı arama motorundan gerçekleşiyor?
        #Backlink
        backlink = self.soup.find_all('span',attrs={"class":'font-4 box1-r'})[0].text
        #Dict key
        info_list = ["Global Rank", "Name of country",
                     "Rank in Country ","Bounce Rate",
                     "Daily Pageviews per Visitor", "Daily Time on Site",
                     "Search Traffic", "Backlink"]
        #Dict value
        result = [global_rank,country_name,
                  country_rank,bounce_rate,
                  views,views_hours,
                  search_engine,backlink]

        # Dict olarak birleşrildi.
        list_to_dict = dict(zip(result,info_list))

        return list_to_dict

    def alaxaKeywords(self) -> dict:
        """5 popüler kelime ve oranı bilgileri verir."""

        # Keywords isimleri depolanacak yer.
        keywords_name = []
        # Keywords % değerlerinin depolanacak yer.
        keywords_value = []

        # Keywords filitre ettik.
        keywords = self.soup.find_all('table', attrs={'id': 'keywords_top_keywords_table'})[0].find_all('span',attrs={"class":""})

        for i in keywords:
            #Dict oluşturabilmek için, iki ayrı liste kayıt ediyoruz.
            if(keywords.index(i) % 2):
                #Key
                keywords_name.append(i.text)
            else:
                #Value
                keywords_value.append((i.text))

        #Dict
        list_to_dict = dict(zip(keywords_name,keywords_value))

        return list_to_dict

    def upstreamSites(self) -> dict:
        """5 adet popüler ziyaretçi alınan siteden ismi ve oranını verir."""

        #Site adları
        site_name = []
        #Site % değerleri
        site_value = []

        # Site adlarının elde edilidği yer.
        ups_site = self.soup.find_all('table', attrs={'id': 'keywords_upstream_site_table'})[0].find_all("a")
        #Site % değerlerin elde edildiği yer.
        ups_value = self.soup.find_all('table', attrs={'id': 'keywords_upstream_site_table'})[0].find_all('span',attrs={"class":""})


        for i in ups_value:
            #Value
            site_value.append(i.text)

        for k in ups_site:
            #Key
            site_name.append(k.text)
        #Dict
        list_to_dict = dict(zip(site_value,site_name))

        return list_to_dict

    def alexaRival(self)->tuple:
        """Ortak ziyaretçiye sahip 5 adet site bilgisi verir. Rakip sitelerde diyebiliriz."""

        #Site adları
        site_name = []
        # Site adlarının elde eldiği yer.
        rival_site = self.soup.find_all('table', attrs={'id': 'audience_overlap_table'})[0].find_all("a")

        for i in rival_site:
            #Site adları
            site_name.append(i.text)

        return tuple(site_name)

    def subDomain(self)->dict:
        """Sub Domainler üzerinden aldığınız trafik yüzdesini gösterir."""

        #Site adları
        site_name = []
        #Site değerleri
        site_value = []

        #Site adların elde eldiği yer.
        sub_name = self.soup.find_all('table', attrs={'id': 'subdomain_table'})[0].find_all("span",attrs={"class":"word-wrap"})
        #Site % lerin elde eldiği yer.
        sub_value = self.soup.find_all('table', attrs={'id': 'subdomain_table'})[0].find_all('span',attrs={"class":""})

        for i in sub_name:
            #Key
            site_name.append(i.text)

        for k in sub_value:
            #Value
             site_value.append(k.text)

        list_to_dict = dict(zip(site_value, site_name))

        return list_to_dict

if __name__ == '__main__':
    alexa = AlexaInfo("python.tc")

    print("Site Genel Bilgiler;")
    print(alexa.alexaInfo())

    print("\nSalexaRivalite 5 popüler keywords")
    print(alexa.alaxaKeywords())

    print("\nZiyaretçilerin nereden geldiği;")
    print(alexa.upstreamSites())

    print("\nRakip Analizi;")
    print(alexa.alexaRival())

    print("\nSubDomain Ziyaretçi Analizi")
    print(alexa.subDomain())

