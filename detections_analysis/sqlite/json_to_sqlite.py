"""
*********************************************************************************************
*    ZADANIEM PROGRAMU JEST WCZYTANIE PLIKÓW Z JSON I PRZEKONWERTOWANIE DO BAZY SQLITE.     *
*     ZOSTANIE TO WYKONANE W NASTEPUJACYCH KROKACH                                          *
*     1) zlistowanie paczek JSON                                                            *
*     a) pobranie do listy nazw                                                             *
*     b) czytanie po kolei plików i dodawanie do nowej listych tych które są widoczne       *
*     c) tworzenie pliku sqlite                                                             *
*                                                                                           *
*     OSTATNIA EDYCJA PLIKU: 04.05.2020                                                     *
*     kontakt z twórcami kodu:                                                              *
*     a) M.Knap mknap@wp.pl                                                                 *
*     b) S.Stuglik slawekstu@gmail.com                                                      *
*********************************************************************************************
"""

#zawsze wrzucam te biblioteki co najczęściej używam - nie sprawdzałem ktore tu sa potrzebne w tym skrypcie
import sqlite3
import json
import os
from os import listdir
import fnmatch#lepsze listowanie plików
from datetime import datetime

#DEFINOWANIE STAŁYCH ŚCIEŻEK
home = os.path.dirname(os.path.abspath(__file__))+"/"#główny katalog z któ©ego odpalamy skrypt
path_detections = home+"detections/"#tam gdzie sa pliki json z detekcjami do wczytania
db = sqlite3.connect('detections.sqlite')
#LISTY i TABLICE
detekcje=[]



#FUNKCJE
#listuj_json() - lista plików w path_detections, wczytanie
def list_json():
    list_files = [x for x in listdir(path_detections) if fnmatch.fnmatch(x,'export_*.json')]
    for file in range (len(list_files)):
        path_file = path_detections+str(list_files[file])
        with open(path_file) as json_file:
                json_from_file = json.load(json_file)
        #dokonczyc
        for detection in json_from_file['detections']:
            stan = "True"
            if str(detection['visible'])==stan:
                detekcje.append(detection)


#Funkcja dodawania do bazy
def sqlite(detekcje):
    print(len(detekcje))

    wzorzec=detekcje[0]
    columns = list(wzorzec.keys())#zobaczmy sobie kolumny jakie sa w json
    sql_base = db.cursor()

    try:
        c.execute("DROP TABLE detections;")#usuawnia - to mozesz pominac, ale to dalem by nie bylo jakis powtorzen
    except:
        w=1
    create_query = "create table if not exists detections (ids INTEGER PRIMARY KEY,{0})".format(" text,".join(columns))
    #print (create_query)#podglad zapytania tworzenia bazy
    query = "insert into detections ({0}) values (?{1})".format(",".join(columns), ",?" * (len(columns)-1))
    #print (query)#podglad zapytania  wstawiania all
    value = []
    values = []
    for data in detekcje:#petla po pojedynczej detekcji
        for i in columns:#petla po nazwach: id, name, frema_content itp
            value.append(str(dict(data).get(i)))#dodawanie wartosci danego parametru(columns)
        values.append(list(value))#lista detekcji gotowych do wrzucenia do bazy
        value.clear()#czyscimy zmienna lokalna

    print("insert has started at " + str(datetime.now()))#sprawdzmy jak dlugo to trwa

    sql_base.execute(create_query)#stworzmy baze jesli jej nie ma
    sql_base.executemany(query , values)#wstawmy cala liste detekcji
    values.clear()#wyczyscmy ta liste - w sumie nie ma znaczenia ale mozna - dla porzadku
    db.commit()

    print("insert has completed at " + str(datetime.now()))#koniec wstawiania - czas
    sql_base.execute('SELECT id FROM detections LIMIT 5;')#przyklad pytan do bazy - jesli istnieje, limit 5 wierszy
    print (sql_base.fetchall())
    sql_base.close()


def main():
    list_json()
    sqlite(detekcje)
#nasz starter - tu odpalamy tylko funkcja nadzorującą -> "main()"
if __name__ == "__main__":
    main()
