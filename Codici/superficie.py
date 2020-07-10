#Script utilizzato per estrarre i dati relativi all'area delle province in km2

import csv 
citta = ["Palermo","Napoli","Roma","Milano","Torino"] # Definiamo la lista delle province che ci servono

def get_data():
    f = open("Superficie province.csv","wt") # Apriamo il file che conterrà solo i dati che ci servono
    writer = csv.writer(f)
    writer.writerow(["Provincia","Superficie totale provincia (Km2)"]) #Scriviamo l'intestazione
    with open("",encoding="utf8",errors='ignore') as file:
        reader = csv.reader(file)
        
        for row in reader:
            if row[1] in citta:
                writer.writerow([row[1],row[3].replace(",",".")])


if __name__ == '__main__':
    get_data()    
    
