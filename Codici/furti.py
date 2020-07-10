import csv

citta = ["Palermo", "Napoli", "Roma", "Milano", "Torino"]   #Definiamo la lista delle province che ci servono

def get_data():
    f = open("Furti di autovetture.csv","wt")        #Apriamo il file che conterrà solo i dati che ci servono
    writer = csv.writer(f)
    writer.writerow(["Provincia","Furti di autovetture"])
    
    f1 = open("Furti in abitazione.csv","wt")        #Apriamo il file che conterrà solo i dati che ci servono
    writer1 = csv.writer(f1)
    writer1.writerow(["Provincia","Furti in abitazione"])
    
    with open("") as file:    
        reader = csv.reader(file)
        
        for row in reader:
            if row[1] in citta:     #Andiamo a filtrare il dataset in base alle province
                if row[9] == "2018":    #Filtriamo in base all'anno
                    if row[5] == "furti di autovetture":    #Filtriamo in base al tipo di delitto
                        writer.writerow([row[1],row[10]])
                    if row[5] == "furti in abitazioni":
                        writer1.writerow([row[1],row[10]])
    f.close()
    f1.close()
    
    
if __name__ == '__main__':
    get_data()
    
