import csv 

citta = ["Palermo","Napoli","Roma","Milano","Torino"] # Definiamo la lista delle province che ci servono

def get_data():
    f = open("Censimento cittadini province.csv","wt") # Apriamo il file che conterrà solo i dati che ci servono
    writer = csv.writer(f)
    writer.writerow(["Provincia","N.Cittadini"]) #Scriviamo l'intestazione
    with open("") as file:
        reader = csv.reader(file)
        
        for row in reader:
            for c in citta:
                if row[1] == c:
                    if row[5] == "totale":  # Aplichiamo i filtri che mi permettono di prendere solo il totale
                        if row[6] == "TOTAL":
                            if row[7] == "totale":
                                if row[9] == "totale":
                                    writer.writerow([row[1],row[12]])

if __name__ == '__main__':
    get_data()    
    
