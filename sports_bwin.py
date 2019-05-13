import requests
from bs4 import BeautifulSoup


stsEkstraklasaURL="https://www.sts.pl/pl/oferta/zaklady-bukmacherskie/zaklady-sportowe/?action=offer&sport=184&region=6502&league=74203&t=1556807180"
answer=requests.get(stsEkstraklasaURL)
if(answer.status_code==200):
    soup=BeautifulSoup(answer.content,'html.parser')  
    
    mecze_i_kursyHTML=soup.find(class_="bet_tab")#wszystkie kursy na stronie w zakładce ekstaklasa 
    
    mecze=mecze_i_kursyHTML.find_all(class_="col3")
        
  
    for mecz in mecze:
        
        data=mecz.thead
           # druzyna1Nazwa=mecz.find(id=True).next_element
           # druzyna1Kurs=mecz.find(id=True).next_element.next_element.next_element
           # remisKurs=mecz.find(class_="event-rates").next_element.next_sibling
           # druzyna2Nazwa=mecz.find(class_="event-rates").next_element.next_sibling.next_sibling.next_element.next_element
           # druzyna2Kurs=mecz.find(class_="event-rates").next_element.next_sibling.next_sibling.next_element.next_element.next_element.next_element       
        if data != None:
            print(data.text)
        else:
            print(data)     
           # print(godzina.text)
           # print(druzyna1Nazwa.text)
           # print(druzyna1Kurs.text)
           # print(druzyna2Nazwa.text)
           # print(druzyna2Kurs.text)
           # print(remisKurs.text)
else:
    print("Błąd: "+str(answer.status_code))