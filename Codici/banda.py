#Script per estrarre i dati relativi agli abbonamenti alla banda ultra larga per ogni provinciai

import csv

citta = ["Palermo", "Napoli", "Roma", "Milano", "Torino"] #Definiamo la lista delle province che ci servono


def get_data():
    f = open("Penetrazione della banda ultra larga.csv","wt") #Apriamo il file che conterrà solo i dati che ci servono
    writer = csv.writer(f)
    writer.writerow(["Provincia","Numero abbonamenti banda larga"]) #Scriviamo l'intestazione 
    
    with open("") as file:    
        reader = csv.reader(file,delimiter=";")
        
        for row in reader:
            if row[16] in citta:    #Andiamo a filtrare il dataset in base alle province 
                writer.writerow([row[16],int(float(row[20]) + float(row[21]) + float(row[22]))]) #Scriviamo nel dataset finale
    f.close()  
            
if __name__ == '__main__':
    get_data()
    
