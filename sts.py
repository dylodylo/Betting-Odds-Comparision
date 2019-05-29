from bs4 import BeautifulSoup
import requests
import re
import json

#Scraping Ekstraklasa STS-website
stsURLleuge="https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=184&region=6502&league=74203&t=1556807180"

#zwraca tablicę linków dla wszystkich możliwych lig piłkarskich ze wszystkich krajów
def getAllLaguesLinks(allLinkstoLague=[]):
    stsURLstronaglowna="https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=184&t=1557777401" 
    leugesLinks=[]
    allLinkstoLague=[]
    x=0
    answer=requests.get(stsURLstronaglowna)
    if answer.status_code==200:
     soup=BeautifulSoup(answer.content,'html.parser')
     druzyny=soup.find(id="sport_184")
     linki=druzyny.find_all(href=True)  
     for link in linki:
        print(str(x)+"stron z"+str(len(linki)))  
        x+=1         
        leugesLinks.append(link.get('href'))        
        for linklig in leugesLinks:
         answer2=requests.get(linklig)
         if answer2.status_code==200:
            soup2=BeautifulSoup(answer2.content,'html.parser')
            names = re.findall(r'league_[0,1,2,3,4,5,6,7,8,9,0]*',str(soup2) )
            for name in names:                
                allLinkstoLague.append({'nazwa':soup2.find(id=str(name)).a.text,'link':soup2.find(id=str(name)).a.get('href')})
                #print(soup2.find(id=str(name)).a.get('href'))
     return allLinkstoLague
    else:
        print('blad')

#scrapowanie kursów ze strony dla danego linku ligi
def scrapMatches(stsURLleuge,wyniki=[]):
 wyniki=[]
 answer=requests.get(stsURLleuge)
 if answer.status_code == 200:
    soup=BeautifulSoup(answer.content,'html.parser')
    mecze=soup.find(class_="shadow_box support_bets_offer")
    dzien=mecze.find_all(class_="col3")
    print(str(len(dzien)))
    if dzien !=None:
        for x in dzien:
                druzyna1Nazwa : str =""
                druzyna2Nazwa : str=""
                druzyna1Kurs : int
                druzyna2Kurs : int
                KursRemis : int                

                if x.thead != None:
                    data=x.thead
                    print("Data meczu:"+data.text)
                kursy=x.find_all(class_="bet bigTip")
                druzyna1=kursy[0].text.split()
                kursremisStr=x.find(class_="bet smallTip").span.text
                druzyna2=kursy[1].text.split()
                for string in druzyna1:
                    if re.match("^\d+?\.\d+?$", string) is None:
                        druzyna1Nazwa+=string
                    else:
                        druzyna1Kurs=float(string)

                for string in druzyna2:
                    if re.match("^\d+?\.\d+?$", string) is None:
                        druzyna2Nazwa+=string
                    else:
                        druzyna2Kurs=float(string)
                    KursRemis=float(kursremisStr)

                print("Drużyna 1: "+druzyna1Nazwa)
                print("Druzyna 1 kurs: "+str(druzyna1Kurs))
                print("Remis: "+str(KursRemis))
                print("Drużyna 2: "+druzyna2Nazwa)
                print("Drużyna 2 kurs: "+str(druzyna2Kurs))
                
                wyniki.append({'druzyna1':druzyna1Nazwa,'kursdruzyna1':druzyna1Kurs,'remis':KursRemis,'druzyna2':druzyna2Nazwa,'kursdruzyna2':druzyna2Kurs})
    return wyniki
 else:
     print("Błąd: "+answer.status_code)
     return None



def startscrappingSTS():
    linkiwszystkichlig=[]
    wszystkiekursy=[]
    linkiwszystkichlig=getAllLaguesLinks([])
    for url in linkiwszystkichlig:
        wszystkiekursy.append(scrapMatches(url,[]))
    with open('pilka.txt', 'w') as outfile:  
        json.dump(wszystkiekursy, outfile)





#Przykład wykorzystania dla ligi mistrzów
#wyn=scrapMatches("https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=184&region=6480&league=15905&t=1558998795",wyniki=[])
#with open('pilka.txt', 'w') as outfile:  
#Przykład dla ligi mistrzów zaciągnięcie kursów
#wyn=scrapMatches("https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=184&region=6480&league=15905&t=1558998795",wyniki=[])
#Przykład dla ligi mistrzów zaciągnięcie kursów
#with open('pilka.txt', 'w') as outfile:  
