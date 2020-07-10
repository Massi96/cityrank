import csv

citta = ["Palermo", "Napoli", "Roma", "Milano", "Torino"] #Definiamo la lista delle province che ci servono

def get_data():
    f = open("Densita di posti letto nelle strutture ricettive.csv","wt")       #Apriamo il file che conterrà solo i dati che ci servono
    writer = csv.writer(f)
    writer.writerow(["Provincia","Totale posti letto nelle strutture ricettive"])                         #Scriviamo l'intestazione
    
    with open("",encoding="utf8",errors='ignore') as file:    
        reader = csv.reader(file)

        for row in reader:
             if row[0] in citta:         #Andiamo a filtrare il dataset in base alle province
                if row[1] == "TOTALE":      #Nel dataset abbiamo una colonna TOTALE che contiene la somma di tutti i posti letto per ogni provincia
                    writer.writerow([row[0],row[54]])#Scriviamo la riga corrispondente

    f.close()
            
            
if __name__ == '__main__':
    get_data()
    
