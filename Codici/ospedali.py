import csv
import re
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

citta = ["PA","NA","RM","MI","TO"] # Definiamo la lista delle province che ci servono
#Poichè nel datase le provice sono indicate con le sigle , definiamo questo dizionario per passare a nominatim il nome completo della provincia
province={"PA":"palermo","MI":"milano","TO":"torino","RM":"roma","NA":"napoli"} 

#Clean ci consente di pulire l'indirizzo per migliorare la ricerca delle coordinate con nominatim
def clean(indirizzo):  
    words = {
        "-":"",
        ",":"",
        "LOC.":"LOCALITA'",
        "P.ZZA":"PIAZZA",
        "N.":"",
        "N°":"",
        "V.":"VIA",
        "V.LE":"VIALE",
        "C.DA":"CONTRADA",
        "SNC.":"",
        "L.GO":"LARGO",
        "PARCO CAFIERO":"",
        "C.SO":"CORSO",
        "(EX VIA ROMA)":"",
        "NONE":"",
        "N[":"",
        "NEMI":""
       }
    
    for key,value in words.items():
        indirizzo = indirizzo.replace(key,value)
    
    return indirizzo

def clean_comune(comune):
    c=comune.replace("A'","à")
    c=comune.replace("E'","è")
    c=comune.replace("I'","ì")
    c=comune.replace("O'","ò")
    c=comune.replace("U'","ù")
    return c

def clean_cap(cap):
    if len(cap) == 3:
        cap = "00" + cap
    if len(cap) == 2:
        cap = "000" + cap
    
    return cap

def get_data():
  f = open("Ospedali e case di cura.csv","wt") # Apriamo il file che conterrà solo i dati che ci servono
  writer = csv.writer(f)
  writer.writerow(["Provincia","Denominazione Strutture","Indirizzo","CAP","Comune","Descrizione tipo struttura","E-mail","Sito web","Latitudine","Longitudine","Cordinate_comune"]) #Scriviamo l'intestazione
  geolocator = Nominatim(user_agent="My-application")
  geocode = RateLimiter(geolocator.geocode,min_delay_seconds=1)
    with open("") as file:
    reader = csv.reader(file)
    
    for row in reader:
        #In alcuni casi nel dataset sono presenti anche i dati relativi alle strutture interne, quindi controlliamo prima quei campi (che nel dataset sono più a destra). 
        if row[12] in citta:            # Andiamo a filtrare il dataset in base alle province
            if row[38] == "":     # row[38]=Struttura interna2 
                if row[24] == "": #row[24]=Struttura interna1
                    #Se row[38] e row[24] sono vuote prendiamo il nome della struttura principale, contenuto in row[9]
                    row[9] = clean(row[9].upper())    # Prima di scrivere sul file puliamo l'indirizzo ed il cap
                    row[10] = clean_cap(row[10])
                    
                    #Ricerca delle coordinate 
                    c = geolocator.geocode(row[9]+","+row[10])
                    
                    if c != None:
                        #Se abbiamo ottenuto le coordinate scriviamo la riga nel file di output
                        #"Provincia","Denominazione Struttura","Indirizzo","CAP","Comune","Descrizione tipo struttura","E-mail","Sito web","Latitudine","Longitudine",Flag per indicare se le coordinate appartengono al comune o meno
                        writer.writerow([province[row[12]],row[7],row[9],row[10],clean_comune(row[11]),row[18],row[16],row[15],c.latitude,c.longitude,0])  
                    else:
                        #Se non abbiamo ottenuto le coordinate della struttura andiamo a cercare le coordinate del comune 
                        c = geolocator.geocode(row[11])
                        #"Provincia","Denominazione Struttura","Indirizzo","CAP","Comune","Descrizione tipo struttura","E-mail","Sito web","Latitudine","Longitudine",Flag per indicare se le coordinate appartengono al comune o meno
                        writer.writerow([province[row[12]],row[7],row[9],row[10],clean_comune(row[11]),row[18],row[16],row[15],c.latitude,c.longitude,1])    
                else:
                    row[26] = clean(row[26].upper()) #indirizzo struttura interna 1
                    row[27] = clean_cap(row[27]) #cap struttura interna 1
                   
                    c = geolocator.geocode(row[26]+" "+row[27]) # Ci facciamo restituire le coordinate della struttura interna
                    
                    if c != None:
                        #"Provincia","Denominazione Strutture","Indirizzo","CAP","Comune","Descrizione tipo struttura","E-mail","Sito web","Latitudine","Longitudine",Flag per indicare se le coordinate appartengono al comune o meno
                        writer.writerow([province[row[12]],row[24],row[26],row[27],clean_comune(row[28]),row[18],row[33],row[32],c.latitude,c.longitude,0])
                    else:
                        c = geolocator.geocode(row[11])
                        #"Provincia","Denominazione Strutture","Indirizzo","CAP","Comune","Descrizione tipo struttura","E-mail","Sito web","Latitudine","Longitudine",Flag per indicare se le coordinate appartengono al comune o meno
                        writer.writerow([province[row[12]],row[24],row[26],row[27],clean_comune(row[28]),row[18],row[33],row[32],c.latitude,c.longitude,1])
            else:
                row[40] = clean(row[40].upper())#row[40],row[41]=indirizzo e cap struttura interna 1
                row[41] = clean_cap(row[41])
                
                c = geolocator.geocode(row[40]+" "+row[41]) # Ci facciamo restituire le coordinate della struttura interna
                
                if c != None:
                    #"Provincia","Denominazione Strutture","Indirizzo","CAP","Comune","Descrizione tipo struttura","E-mail","Sito web","Latitudine","Longitudine",Flag per indicare se le coordinate appartengono al comune o meno
                    writer.writerow([province[row[12]],row[38],row[40],row[41],clean_comune(row[42]),row[18],row[47],row[46],c.latitude,c.longitude,0])
                else:
                    c = geolocator.geocode(row[11]) #row[11]= comune
                    #"Provincia","Denominazione Strutture","Indirizzo","CAP","Comune","Descrizione tipo struttura","E-mail","Sito web","Latitudine","Longitudine",Flag per indicare se le coordinate appartengono al comune o meno
                    writer.writerow([province[row[12]],row[38],row[40],row[41],clean_comune(row[42]),row[18],row[47],row[46],c.latitude,c.longitude,1])
    f.close()
if __name__ == '__main__':
    get_data()
    
