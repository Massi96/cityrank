#Script usato per estrarre i dati revativi alla natalità, mortalità e vecchiaia per ogni provincia

import csv

citta = ["Palermo", "Napoli", "Roma", "Milano", "Torino"] #Definiamo la lista delle province che ci servono

#Definizione degli indicatori da estrarre dal dataset
ind1 = "tasso di natalità (per mille abitanti)"
ind2 = "indice di vecchiaia (valori percentuali) - al 1° gennaio"
ind3 = "tasso di mortalità (per mille abitanti)"

anno1 = "2018"
anno2 = "2019"

def get_data():
    f = open("Tasso di natalità.csv","wt")       #Creazione dataset tasso di natalità
    writer = csv.writer(f)
    writer.writerow(["Provincia","Tasso di natalità"])      #Scriviamo l'intestazione
    
    f1 = open("Indice di vecchiaia.csv","wt")#Creazione dataset indice di vecchiaia
    writer1 = csv.writer(f1)
    writer1.writerow(["Provincia","Indice di vecchiaia"])
    
    f2 = open("Tasso di mortalità.csv","wt")#Creazione dataset tasso di mortalità
    writer2 = csv.writer(f2)
    writer2.writerow(["Provincia","Tasso di mortalità"])
    
    with open("") as file:
        reader = csv.reader(file)
        #Il dataset iniziale contiene dati che vanno dal 2016 al 2019, quindi sono oppurtuni alcuni filtraggi
        for row in reader:
            if row[1] in citta:       #Andiamo a filtrare il dataset in base alle province
                if row[5] == anno1:     #Andiamo a filtrare il dataset in base all'anno
                    if row[3] == ind1:      #Andiamo a filtrare il dataset in base ai tassi 
                        writer.writerow([row[1],row[6]])
                    if row[3] == ind3:
                        writer2.writerow([row[1],row[6]])
                if row[5] == anno2: #I dati più recenti riguardanti l'indice di vecchiaia sono presenti solo per il 2018
                    if row[3] == ind2:
                        writer1.writerow([row[1],row[6]])
    f.close()
    f1.close()
    f2.close()
    
if __name__ == '__main__':
    get_data()
    
