#Script per il calcolo di disoccupazione (giovanile e non) per ogni provincia

import csv
import re

citta = ["Palermo", "Napoli", "Roma", "Milano", "Torino"] #Definiamo la lista delle province che ci servono

def get_data():
    f = open("","wt")        #Creiamo il file che conterrà il tasso di disoccupazione totale
    writer = csv.writer(f)
    writer.writerow(["Provincia","Tasso di disoccupazione"])             #Scriviamo l'intestazione
    
    f1 = open("","wt")   #Creiamo il file che conterrà il tasso di disoccupazione giovanile  
    writer1 = csv.writer(f1)
    writer1.writerow(["Provincia","Tasso di disoccupazione giovanile"])#Scriviamo l'intestazione
    
    with open("") as fi:
       reader = csv.reader(fi)
       
       for row in reader:
            if row[1] in citta:             #Andiamo a filtrare il dataset in base alle province
                if row[5] == "totale":      #Prendiamo il totale tra maschi e femmine 
                    if row[8] == "2019":    #Andiamo a filtrare il dataset in base all'anno
                        if row[7] == "15-74 anni":  #In base alla classe d'età scriviamo in un file piuttosto che nell'altro
                            writer.writerow([row[1],str(row[10]).replace(",",".")])
                        if row[7] == "15-29 anni":
                            writer1.writerow([row[1],str(row[10]).replace(",",".")])
    f.close()
    f1.close()

if __name__ == '__main__':
    get_data()
    
