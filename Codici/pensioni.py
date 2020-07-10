import csv
import re

citta = ["Milano", "Torino","Palermo","Roma","Napoli"] #Definiamo la lista delle province che ci servono

def get_data():
    #I dati delle pensioni sono contenuti in più file csv, questi contengono i dati delle pensioni divisi per le zone d'italia, ad esempio nord,sud o centro
    f = open("") 
    f1 = open("")
    f2 = open("")
    f3 = open("")
    reader = csv.reader(f)
    reader1 = csv.reader(f1)
    reader2 = csv.reader(f2)
    reader3 = csv.reader(f3)
    
    final = open("Importo medio delle pensioni di vecchiaia.csv","wt")       #Unifichiamo tutti i dati in un singolo file
    writer = csv.writer(final)
    writer.writerow(["Provincia","Importo medio delle pensioni di vecchiaia"])      #Scriviamo l'intestazione
    
    # Il replace serve perchè nei dataset gli importi sono scritti con l2 ","
    for row in reader:
        if row[2] in citta:
            writer.writerow([row[2],'%.2f'%float(row[4].replace(",","."))])
    for row in reader1:
        if row[1] in citta:
            writer.writerow([row[1],'%.2f'%float(row[3].replace(",","."))])
    for row in reader2:
        if row[2]  in citta:
            writer.writerow([row[2],'%.2f'%float(row[4].replace(",","."))])
    for row in reader3:
        for c in citta:
            if row[2] == c:     #I dati di Milano e Torino sono contenuti in un singolo file
                writer.writerow([row[2],'%.2f'%float(row[4].replace(",","."))])
    
    f.close()
    f1.close()
    f2.close()
    f3.close()
    final.close()

if __name__ == '__main__':
    get_data()
    
