#Script per calcolare la differenza di tasso d'occupazione tra maschi e femmine

import csv
import re

def get_data():
  with open("Differenza fra tasso di occupazione maschile e femminile.csv","wt") as file:    #Apriamo il file che conterrà solo i dati che ci servono
    writer = csv.writer(file) 
    writer.writerow(["Provincia","Differenza fra tasso di occupazione maschile e femminile"])          #Scriviamo l'intestazione
    
    #Definiamo un dizionario che ci serve per tenere traccia dei tassi di occupazione per ogni provincia, divisi per sesso
    tassi = {"Torino":{"maschi":0,"femmine":0},"Napoli":{"maschi":0,"femmine":0},          
             "Roma":{"maschi":0,"femmine":0},"Milano":{"maschi":0,"femmine":0},
             "Palermo":{"maschi":0,"femmine":0}}      
     
    citta = ["Palermo", "Napoli", "Roma", "Milano", "Torino"] #Definiamo la lista delle province che ci servono 
    reader = csv.reader(open(""))
       
    for row in reader:
        if row[1] in citta:      #Andiamo a filtrare il dataset in base alle province
            if row[5] != "totale":  #Ci interessano i tassi di maschi e femmine, non il totale
                if row[7] == "15-64 anni":      #Andiamo a filtrare il dataset in base alla classe d'età 
                    if row[9] == "2019":        #Andiamo a filtrare il dataset in base all'anno
                        tassi[row[1]][row[5]] = row[10]
    for key in tassi.keys():
        writer.writerow([key,str(float(tassi[key]["maschi"])-float(tassi[key]["femmine"]))])  #Scriviamo la differenza convertita in stringa


if __name__ == '__main__':
    get_data()