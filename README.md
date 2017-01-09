Accessing alexa information through Python

**Python aracılığıyla alexa bilgilerine erişme**

Merhabalar, alexa.com dünya çapında siteleri analiz eder. Bu paket sayesinde bu verilere erişim sağlayacaksınız.

# Kullanımı

İlk olarak, paketi yüklemek ile başlayabiliriz.

    sudo pip install git+https://github.com/AliYmn/Python-Alexa

Alexa paketini, kullanacağınız modüle ekleyin.

    from alexa import AlexaInfo

Constructor'ı çağırıp, "site url" belirtmeniz yeterli olucaktır. Site url belirtirken
**başında** http/https olmadan direk domain adı yazın. Örneğin : python.tc
 
    alexa = AlexaInfo("python.tc")

Şimdi fonksiyonlarımızı çağıralabiliriz.

**Alexa Genel Bilgiler**

Global Rank, Ülke adı , Ülke Rank gibi bilgilere ulaşabildiğiniz fonksiyondur.

    alexa.alexaInfo()
    
 **Alexa Keywords Bilgileri**
 
 5 adet pöpüler aranan kelimeyi yüzde olarak verir.
 
    alexa.alaxaKeywords()

**Alexa Ziyaretçi Aldığınız Siteler**

En çok ziyaretçi aldığınız 3 adet siteyi yüzde olarak verir.

    alexa.upstreamSites()
    
 **Alexa Subdomain Analizi**
 
 Subdomain üzerinden aldığınız ziyaretçileri yüzde olarak bilgisini verir.
 
     alexa.subDomain()

**Alexa Rakip Analizi**

Ortak ziyaretçiye sahip olduğunuz siteleri listeler.

    alexa.alexaRival()
    
    
# Örnek Kullanım

    from alexa import AlexaInfo
    
    result = AlexaInfo("python.tc")
    
    print("Site Genel Bilgiler;")
    print(result.alexaInfo())
    
    print("\nSite 5 popüler keywords")
    print(result.alaxaKeywords())
    
    print("\nZiyaretçicilerin nereden geldiği;")
    print(result.upstreamSites())
    
    print("\nRakip Analizi;")
    print(alexa.alexaRival())
    
    print("\nSubDomain Ziyaretçi Analizi")
    print(result.subDomain())


**Output :**

    Site Genel Bilgiler;
    {'747,709': 'Global Rank', 'Turkey': 'Name of country', '19,718': 'Rank in Country ', '46.20%': 'Bounce Rate', '4.40': 'Daily Pageviews per Visitor', '4:37': 'Daily Time on Site', '16.80%': 'Search Traffic', '84': 'Backlink'}
    
    Site 5 popüler keywords;
    {'50.54%': 'python nedir', '21.89%': 'python türkiye', '3.49%': 'python.tc', '2.09%': 'pyton nedir', '1.90%': 'python wordpress'}
    
    Ziyaretçilerin nereden geldiği;
    {'28.4%': 'google.com.tr', '10.5%': 'wmaraci.com', '7.4%': 'facebook.com'}
    
    Rakip Analizi;
    ('pythondersleri.com', 'istihza.com', 'ysar.net', 'djangoturkiye.com', 'halitalptekin.com')
    
    SubDomain Ziyaretçi Analizi
    {'98.70%': 'python.tc'}
    
 Bilgileri http://www.alexa.com/siteinfo/python.tc üzerinden karşılaştırabilirsiniz...
