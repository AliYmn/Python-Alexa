from bs4 import BeautifulSoup
import urllib.request

"""
Bu modül, Alexa.com üzerinden sitelerin analiz bilgilerini elde etmeye yaramaktadır.
"""

class AlexaInfo():
    def __init__(self,url=str()):
        """
        # Arguments #
        url:str()         | String formatında url bilgisi almaktadır.

        # Properties #
        url:str()         | İstekte bulunan url alexa üzerinden taranır ve bilgiler verilir.
        """

        self.url = url
        # Html kodların kompleks şekilde bir arada bulunur.
        soup = BeautifulSoup(urllib.request.urlopen("http://www.alexa.com/siteinfo/{}".format(self.url)),'html.parser')
        self.soup = soup

    def ranks(self) -> dict:
        """
        Alexa.com üzerinden, genel rankların bilgisini verdiği fonksiyondur.

        # Properties #
        global_rank         | Sitenin, global ülke puanı.
        country_rank        | Sitenin, ülke içerisindeki puanı.
        bounce_rate         | Alexa üzerinde puan yükseltme oranı.
        views               | Sitenin, görüntülenme yüzdesi.
        views_hours         | Sitenin, saatlik görütünlenme yüzdesi
        search_engine       | Arama motorunda aranma hacmi
        backlink            | Alexa backlink değeri.

        """

        #Eğer site yeniyle, default '0' değeri atamaktadır.
        #Veriables
        global_rank, country_rank, bounce_rate, views, views_hours, search_engine, backlink = "0","0","0","0","0","0","0"

        # Rankları filitre ettik.
        rank = self.soup.find_all('strong', attrs={'class': 'metrics-data align-vmiddle'})

        #Elde edilen bilgileri,değişkenlere aktar
        country_name = self.soup.find_all('span', attrs={'class': 'countryRank'})[0].find("h4").find("a").text
        global_rank = rank[0].text.strip() # Dünya Rankı
        country_rank = rank[1].text.strip()# Ülke rankı
        bounce_rate = rank[2].text.strip() # Çıkma Oranı
        views = rank[3].text.strip() # Günlük ziyaretçi başına düşen, görüntülenme sayısı
        views_hours = rank[4].text.strip() # Sitedeki günlük saat görüntülenme sayısı

        #Serach_engine kontrol
        if(len(rank) == 5):
            rank.insert(4,"")

        # Aranma Hacmi
        search_engine = rank[5].text.strip()
        # Alexa backlink
        backlink = self.soup.find_all('span',attrs={"class":'font-4 box1-r'})[0].text

        #Dict Key
        info_list = ["Global Rank", "Name of country",
                     "Rank in Country ", "Bounce Rate",
                     "Daily Pageviews per Visitor","Daily Time on Site",
                     "Search Traffic", "Backlink"]
        #Dict Value
        result = [global_rank,country_name,country_rank,bounce_rate,views,views_hours,search_engine,backlink]

        #Dict
        list_to_dict = dict(zip(result,info_list))

        return list_to_dict

    def keywords(self) -> dict:
        """5 popüler kelime ve oranı bilgileri verir.

        # Properties #
        keywords_name         | Keywords adlarını tutar.
        keywords_value        | keywrods yüzdelerini tutar.

        """

        #Veriables
        keywords_name = []
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

    def visit(self)->dict:
        """En çok ziyaret gelen siteleri listeler.

        # Properties #
        site_name        | site adlarını tutar.
        site_value       | site yüzdelerini tutar.

        """

        #Veriables
        site_name = []
        site_value = []

        #Bilgileri ayrıştılıyor.
        visit_site = self.soup.find_all('table', attrs={'id': 'keywords_upstream_site_table'})[0].find_all("a")
        visit_value = self.soup.find_all('table', attrs={'id': 'keywords_upstream_site_table'})[0].find_all('span',attrs={"class":""})

        for i in visit_value:
            #Key
            site_value.append(i.text)

        for k in visit_site:
            #Value
            site_name.append(k.text)

        #Dict
        list_to_dict = dict(zip(site_value,site_name))

        return list_to_dict

    def rival(self) -> tuple:
        """Ortak ziyaretçiye sahip 5 adet site bilgisi verir. Rakip sitelerde diyebiliriz.

        # Properties #
        site_name        | site adlarını tutar.

        """

        #Veriables
        site_name = []

        #Bilgiler alınıyor.
        rival_site = self.soup.find_all('table', attrs={'id': 'audience_overlap_table'})[0].find_all("a")

        for i in rival_site:
            #Value
            site_name.append(i.text)

        return tuple(site_name)

    def sub_domain(self) -> dict:
        """Sub Domainler üzerinden aldığınız trafik yüzdesini gösterir.

        # Properties #
        site_name        | site adlarını tutar.
        site_value       | site yüzdelerini tutar.

        """

        #Veriables
        site_name = []
        site_value = []

        #Bilgiler alınıyor.
        sub_name = self.soup.find_all('table', attrs={'id': 'subdomain_table'})[0].find_all("span",attrs={"class":"word-wrap"})
        sub_value = self.soup.find_all('table', attrs={'id': 'subdomain_table'})[0].find_all('span',attrs={"class":""})

        for i in sub_name:
            #Key
            site_name.append(i.text)

        for k in sub_value:
            #Value
             site_value.append(k.text)
        #Dict
        list_to_dict = dict(zip(site_value, site_name))

        return list_to_dict

    def people(self):
        " Kadınların,erkeklerin,öğrencilerin ve çalışanların vb. kriterlere göre ziyaret analizilerini bulundurur."

        #Veriables
        style = []
        result = []
        count = 0


        while True:
            try:
                for i in self.soup.find_all('span',attrs={'class':'pybar-bg'})[count].find_all('span'):
                    value = i.get('style')[6:9]
                    result = result + value.split('%')
                    count = count+1

            except:
                break

        for k in result:
            #Filitre edip, sadece oranları al.
            if(k == '%' or k == ';' or k==""):
                pass
            else:
                style.append(k)

        male = (int(style[0])+int(style[1]))/2
        female = (int(style[2])+int(style[3]))/2
        no_college = (int(style[4])+int(style[5]))/2
        some_college = (int(style[6])+int(style[7]))/2
        graduate_school = (int(style[8])+int(style[9]))/2
        college = (int(style[10])+int(style[11]))/2
        home = (int(style[12])+int(style[13]))/2
        school = (int(style[14])+int(style[15]))/2
        work = (int(style[16])+int(style[17]))/2

        #Key
        key = ['male','female','no_college','some_college','graduate_scholl','home','school','work']
        #Value
        value = [male,female,no_college,some_college,graduate_school,college,home,school,work]

        #Dict
        list_to_dict = dict(zip(key, value))

        return list_to_dict

if __name__ == '__main__':
    alexa = AlexaInfo("python.tc")

    print("Site Genel Bilgiler;")
    print(alexa.ranks())

    print("\nSalexaRivalite 5 popüler keywords")
    print(alexa.keywords())

    print("\nZiyaretçilerin nereden geldiği;")
    print(alexa.visit())

    print("\nRakip Analizi;")
    print(alexa.rival())

    print("\nSubDomain Ziyaretçi Analizi")
    print(alexa.sub_domain())

    print("\nİnsanların ziyaret analizi")
    print(alexa.people())