import requests
from bs4 import BeautifulSoup




forBetEkstraklasaURL="https://www.iforbet.pl/oferta/8/29994"
answer=requests.get("https://www.iforbet.pl/oferta/8/29994")
if(answer.status_code==200):
    soup=BeautifulSoup(answer.content,'html.parser')  
    mecze_i_kursyHTML=soup.find_all(class_="events-group")#wszystkie kursy na stronie w zakładce ekstaklasa 
    for dzien in mecze_i_kursyHTML :
        data=dzien.find(class_="event-start")
        mecze=dzien.find_all(class_="details")

        for mecz in mecze:
            godzina=mecz.find(class_="event-time")
            druzyna1Nazwa=mecz.find(id=True).next_element
            druzyna1Kurs=mecz.find(id=True).next_element.next_element.next_element
            remisKurs=mecz.find(class_="event-rates").next_element.next_sibling
            druzyna2Nazwa=mecz.find(class_="event-rates").next_element.next_sibling.next_sibling.next_element.next_element
            druzyna2Kurs=mecz.find(class_="event-rates").next_element.next_sibling.next_sibling.next_element.next_element.next_element.next_element       
            print(data.text)     
            print(godzina.text)
            print(druzyna1Nazwa.text)
            print(druzyna1Kurs.text)
            print(druzyna2Nazwa.text)
            print(druzyna2Kurs.text)
            print(remisKurs.text)
else:
    print("Błąd: "+answer.status_code)