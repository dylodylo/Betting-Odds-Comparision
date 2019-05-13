from bs4 import BeautifulSoup
import requests
import re

#Scraping Ekstraklasa STS-website
stsURL="https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=184&region=6502&league=74203&t=1556807180"
wyniki=[]
answer=requests.get(stsURL)
if answer.status_code == 200:
    soup=BeautifulSoup(answer.content,'html.parser')
    mecze=soup.find(id="offerTables")
    dzien=mecze.find_all(class_="col3")
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

                print("Drużyna 1: "+druzyna1[0])
                print("Druzyna 1 kurs: "+druzyna1[1])
                print("Remis: "+kursremisStr)
                print("Drużyna 2: "+druzyna2[0])
                print("Drużyna 2 kurs: "+druzyna2[1])
                
                wyniki.append({'druzyna1':druzyna1Nazwa,'kursdruzyna1':druzyna1Kurs,'remis':KursRemis,'druzyna2':druzyna2Nazwa,'kursdruzyna2':druzyna2Kurs})
else:
    print("Błąd: "+answer.status_code)
