#CEL: wczytanie pliku json i konwersja na plik .db
#AUTOR: Justyna Medrala
#OSTATNIA MODYFIKACJA: 15.07.2020

import json
import os
import sqlite3
import random

string = "Detections_analysis/sqlite/"
home = os.path.dirname(os.path.abspath(__file__)) + '/'
back_to_main_path = home[:-len(string)]
main_data_path = back_to_main_path+"data_save/Detections_analysis/"
detections_path = main_data_path+"anti-artefact/after_filtr/good/"
save_path = main_data_path+"sqlite/"

def list_path(adres):
    #wszystkie pliki json z danymi
    list_file = os.listdir(adres)
    return list_file

def read_json(path, list):
    #wczytuje konkretny plik w formacie json np. drugi z mojej listy plikow
    data = json.load(open(path+list[1]))
    return data


def create_sqlite(columns, values):
    """    #tworzy plik .db
    # randint zbedne, przy tworzeniu bazy drugi dopisuje po raz kolejny wartosci do tej samej,
    # mozna stworzyc zabezpieczenie przed otwieraniem tego samego pliku z danymi kilka razy
    """
    print(save_path+str(values[random.randint(0,len(values)-1)][0])+".db")
    db = sqlite3.connect(save_path+str(values[random.randint(0,len(values)-1)][0])+".db")
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS detections;")
    c.execute("CREATE TABLE if not exists detections (ids INTEGER PRIMARY KEY,{0})".format(" text,".join(columns)))

    for x in range(len(values)): #ewentualnie uzycie executemany
        sql = "INSERT INTO detections ({0}) VALUES (?{1})".format(",".join(columns), ",?" * (len(columns)-1))
        c.execute(sql, values[x])
    db.commit()
    db.close()

def col(data):
    #zwraca nazwy kolumn
    b = data['detections'][0]
    columns = list(b.keys())
    return columns

def val(data):
    #zwraca wartosci
    value = []
    values = []
    for a in data['detections']:
        for it, val in a.items():
            value.append(val)
        values.append(value[:])
        value = []
    return values

def main():
    list_file = list_path(detections_path)
    data = read_json(detections_path, list_file)
    columns = col(data)
    values = val(data)
    create_sqlite(columns, values)

if __name__ == "__main__":
    main()