import csv
import pandas as pd
from pandas import DataFrame
import re

# Il dizionario "province" contiene coppie del tipo Sigla_provincia-[Provincia,reddito_totale]
province={"PA":["Palermo",0],"MI":["Milano",0],"0":["Napoli",0],"RM":["Roma",0],"TO":["Torino",0]}

# Il dizionario contrib_tot contiene coppie del tipo Sigla_provincia-Numero_totale_contribuenti
contrib_tot={"PA":0,"MI":0,"0":0,"RM":0,"TO":0}

# la funzione clean utilizza la libreria pandas per riempire le celle vuote 
def clean():
    df=DataFrame(pd.read_csv("",sep=";"))
    df.fillna(0).to_csv("Reddito_medio.csv",sep=",",index=None)

def get_data():
    with open("","w",newline="") as f:
        
        file_output=csv.writer(f) #Inizializzo il file di output
        file_output.writerow(["Provincia","Reddito medio complessivo per contribuente"]) #Scrivo la riga d'intestazione
        file_input=csv.reader(open("Reddito_medio.csv","r")) #Lettura del file di input
        for row in file_input:
            #Per ogni riga controllo che la sigla della provincia (contenuta in row[4]) sia una delle chiavi del diz province
            if row[4] in province.keys():
                #Aggiorno il totale del reddito e dei contribuenti per quella provincia
                #Il dataset divide i contribuenti in categorie (ed. lavoratore autonomo o dipendente) per cui i dati sono divisi tra le varie colonne
                province[row[4]][1]+=float(row[35])+float(row[37])+float(row[39])+float(row[41])+float(row[43])+float(row[45])+float(row[47])+float(row[49])
                contrib_tot[row[4]]+=int(row[7])
        
        for prov in province.keys():
            #Finito di leggere il file di input vado a scrivere i risultati nel file finale
            reddito_medio = province[prov][1]/contrib_tot[prov] 
            file_output.writerow([province[prov][0],'%.2f'%float(reddito_medio)])
            
if __name__ == '__main__':
    clean()
    get_data()
