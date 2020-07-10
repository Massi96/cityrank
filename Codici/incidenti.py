import csv

citta = ["Palermo", "Napoli", "Roma", "Milano", "Torino"] #Definiamo la lista delle province che ci servono


def get_data():
    f = open("Incidenti Stradali.csv","wt")     #Apriamo il file che conterrà solo i dati che ci servono
    writer = csv.writer(f)
    writer.writerow(["Provincia","Totale morti e feriti"])      #Scriviamo l'intestazione
    with open("",encoding="latin-1") as f2:    
        reader = csv.reader(f2,delimiter=";")
        
        for row in reader:
            if row[0].strip() in citta:          #Il nome delle province nel dataset aveva degli spazi ad inizio stringa 
                writer.writerow([row[0].strip(),row[13]])
    f.close()

if __name__ == '__main__':
    get_data()
    
