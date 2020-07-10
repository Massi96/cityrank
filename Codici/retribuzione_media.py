import csv

citta = ["Palermo", "Napoli", "Roma", "Milano", "Torino"] #Definiamo la lista delle province che ci servono
dato = "Retribuzione lorda oraria per ora retribuita delle posizioni lavorative dipendenti in euro (media). " #Definiamo la stringa che contiene il tipo di dato

def get_data():
    f = open("Retribuzione media.csv","wt")  #Apriamo il file che conterrà solo i dati che ci servono
    writer = csv.writer(f)
    writer.writerow(["Provincia","Retribuzione media"])     #Scriviamo l'intestazione
    with open("") as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            if row[1] in citta:     #Andiamo a filtrare il dataset in base alle province
                if row[3] == dato:      #Andiamo a filtrare il dataset in base al tipo di dato
                    if row[5] == "totale":  #Prendiamo il totale tra maschi e femmine 
                        writer.writerow([row[1],row[8]])
    f.close()

if __name__ == '__main__':
    get_data()
    
