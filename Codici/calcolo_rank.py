# Questo codice ci permette di fare il merge fra tutti i dataset che abbiamo ripulito
# Utilizziamo pandas per facilitare l'operazione di merge, inoltre andiamo a relazionare alcuni dati con la superficie e il numero degli abitanti della provincia
import pandas as pd
import csv
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


#Questa funzione prende in input un dataset ci permette di contare il numero delle strutture presenti in ogni provincia,ovvero ospedali,scuole e biblioteche
def count(nome_file):
    
    l= {"palermo":0,"milano":0,"napoli":0,"roma":0,"torino":0}
    l=l.fromkeys(l, 0)
    
    df = pd.read_csv(nome_file,keep_default_na=False,encoding="latin-1")  # Keep_default_na=False ci serve per evitare che riconosca la sigla di napoli come "nan"
    df.columns = df.columns.str.lower() # Portiamo in minuscolo i nomi di tutte le colonne in modo da far corrispondere i nomi delle province alle chiavi del dizionario
    df.provincia=df.provincia.str.lower()
    province=df["provincia"].unique().tolist()
    for prov in province:
        l[prov]=df[df["provincia"]==prov]["provincia"].count()
    
    return l.values()


# Questa funzione ci serve per il calcolo delle coordinate della provincia
def coordinate(finale):
    lat = []
    long = []
    with open("Output_finale.csv") as fin:
        reader = csv.reader(fin)
        next(reader)
         
        for row in reader:
           geolocator = Nominatim(user_agent="My-application")
           geocode = RateLimiter(geolocator.geocode,min_delay_seconds=1)
           c = geolocator.geocode(row[0])
           
           lat.append(c.latitude)
           long.append(c.longitude)
        
        finale["Latitudine"] = lat
        finale["Longitudine"] = long
            
            
# Questa funzione mi permette di relazionare alcuni dati del Dataframe con il numero dei cittadini
def relate(f):
    
    # I degli indicatori vengono divisi per il numero degli abitanti della provincia 
    f["Percentuale_abbonamenti_banda_larga_su_popolazione_residente"]=((f["Percentuale_abbonamenti_banda_larga_su_popolazione_residente"] / f["Popolazione_residente"]) *100).round(2)
    f["Totale_morti_e_feriti_in_incidenti_per_100000_abitanti"] = ((f["Totale_morti_e_feriti_in_incidenti_per_100000_abitanti"] / f["Popolazione_residente"]) *100000).round(2)
    f["Furti_in_abitazione_ogni_100000_abitanti"] = ((f["Furti_in_abitazione_ogni_100000_abitanti"] / f["Popolazione_residente"]) *100000).round(2)
    f["Furti_di_autovetture_ogni_100000_abitanti"]= ((f["Furti_di_autovetture_ogni_100000_abitanti"] / f["Popolazione_residente"]) *100000).round(2)
    f["Rapporto_superficie_N_Ospedali"] = (f["Superficie_provincia(Km2)"]/ f["N.Ospedali"]).round(2)
    f["Rapporto_superficie_N_Scuole"] = (f["Superficie_provincia(Km2)"]/ f["N.Scuole"]).round(2)
    f["Numero_biblioteche_ogni_10000_abitanti"] = ((f["N.Biblioteche"]/ f["Popolazione_residente"])*10000).round(2)

    
def merge():
    #Lettura dei dataset
    reddito = pd.read_csv("")
    retribuzione = pd.read_csv("")
    pensioni = pd.read_csv("")
    rifiuti = pd.read_csv("")
    incidenti = pd.read_csv("")
    furti_auto = pd.read_csv("")
    furti_casa = pd.read_csv("")
    tasso_disoccupazione = pd.read_csv("")
    tasso_disoccupazione_g = pd.read_csv("")
    diff_tasso = pd.read_csv("")
    tasso_natalita = pd.read_csv("")
    tasso_mortalita = pd.read_csv("")
    indice_v = pd.read_csv("")
    posti = pd.read_csv("")
    banda = pd.read_csv("")
    popolazione = pd.read_csv("")
    superficie = pd.read_csv("")
    
    #Facciamo il merge dei dataset in base alla provincia
    f = pd.DataFrame()
    f = pd.merge(reddito,retribuzione,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,pensioni,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,rifiuti,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,incidenti,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,furti_auto,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,furti_casa,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,tasso_disoccupazione,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,tasso_disoccupazione_g,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,diff_tasso,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,tasso_natalita,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,tasso_mortalita,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,indice_v,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,posti,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,banda,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,popolazione,how="inner",left_on="Provincia",right_on="Provincia")
    f = pd.merge(f,superficie,how="inner",left_on="Provincia",right_on="Provincia")
    
    # Arrotondiamo alcuni valori alla seconda cifra decimale
    f["Tasso di disoccupazione giovanile"]=f["Tasso di disoccupazione giovanile"].round(2)
    f["Tasso di disoccupazione"]=f["Tasso di disoccupazione"].round(2)
    f["Differenza fra tasso di occupazione maschile e femminile"]=f["Differenza fra tasso di occupazione maschile e femminile"].round(2)
    
    # Aggiungo al Dataframe il numero di biblioteche, scuole e ospedali e case di cura
    f["N.Ospedali"] = count("Progetto-Open-Data/dataset/Ospedali e case di cura.csv")
    f["N.Scuole"] =count("Progetto-Open-Data/dataset/scuole.csv")
    f["N.Biblioteche"] =count("Progetto-Open-Data/dataset/Biblioteche.csv")
    
    # Rinominiamo le colonne per rendere il file leggibile da umap
    f.rename(columns={"Retribuzione media":"Retribuzione_media",
                      "Importo medio delle pensioni di vecchiaia":"Importo_medio_delle_pensioni_vecchiaia",
                      "Raccolta rifiuti urbani(kg/abitante)":"Raccolta_rifiuti_urbani_kg_abitante",
                      "Reddito medio complessivo per contribuente":"Reddito_medio_complessivo_per_contribuente",
                      "N.Cittadini":"Popolazione_residente",
                      "Numero abbonamenti banda larga":"Percentuale_abbonamenti_banda_larga_su_popolazione_residente",
                      "Totale morti e feriti": "Totale_morti_e_feriti_in_incidenti_per_100000_abitanti",
                      "Furti di autovetture": "Furti_di_autovetture_ogni_100000_abitanti", 
                      "Furti in abitazione":"Furti_in_abitazione_ogni_100000_abitanti",
                      "Raccolta differenziata(%)":"Raccolta_differenziata","Tasso di natalità":"Tasso_di_natalita","Tasso di mortalità":"Tasso_di_mortalita",
                      "Indice di vecchiaia":"Indice_vecchiaia",
                      "Differenza fra tasso di occupazione maschile e femminile":"Differenza_tasso_occupazione_maschile_femminile",
                      "Totale posti letto nelle strutture ricettive":"Totale_posti_letto_strutture_ricettive","Popolazione residente":"Popolazione_residente",
                      "Superficie totale provincia (Km2)":"Superficie_provincia(Km2)","Differenza tasso occupazione maschile e femminile":"Differenza_tasso_occupazione_maschile_femminile",
                      "Tasso di disoccupazione":"Tasso_disoccupazione","Tasso di disoccupazione giovanile":"Tasso_disoccupazione_giovanile"},inplace=True)

    relate(f)
    
    f.to_csv("Output_finale.csv",index=False,sep=",")    
    
# Questa funzione ci permette di calcolare l'indice di vivibilità per ogni provincia
def calcoloRank():
    punteggi=[]
    finale = pd.read_csv("Output_finale.csv")
    
    # in crescenti ci sono gli indicatori che vanno ordinati in maniera inversa poichè più basso è il valore più è alto il punteggio ottenuto per quell'indicatore
    crescenti=["Raccolta_rifiuti_urbani(kg/abitante)","Totale_morti_e_feriti_in_incidenti_per_100000_abitanti","Furti_di_autovetture_ogni_100000_abitanti",   
                "Furti_in_abitazione_ogni_100000_abitanti","Tasso_disoccupazione","Tasso_disoccupazione_giovanile", 
                "Differenza_tasso_occupazione_maschile_femminile","Tasso_mortalita","Indice_vecchiaia",  #    
                "Rapporto_superficie_N_Ospedali","Rapporto_superficie_N_Scuole","Numero_biblioteche_ogni_10000_abitanti"]    # 
    
    # Questa lista esclude le colonne che non devono essere incluse nel calcolo dell'indice
    nonConsiderare=["Popolazione_residente","Superficie_provincia(Km2)","N.Ospedali","N.Scuole","N.Biblioteche"] 
    
    # Questi dizionari servono per stilare le classifiche in base alle quali calcoliamo il punteggio finale
    classifica = {"Palermo":0,"Milano":0,"Napoli":0,"Roma":0,"Torino":0} 
    parziali = {"Palermo":0,"Milano":0,"Napoli":0,"Roma":0,"Torino":0}
    
    
    for colonna in finale.columns:
        score=0.5    
        #Controlliamo che la colonna corrente sia valida per il calcolo dell'indice
        if ((colonna !="Provincia" ) and (colonna not in nonConsiderare)):
            
            
            if colonna in crescenti:
                #in lista mettiamo le province ordinate in base al valore dell'indicatore considerato
                lista = finale.sort_values(by=[colonna])["Provincia"].tolist() 
               
                for item in lista:
                    parziali[item]=score
                    classifica[item]+=score
                    score-=0.1
                    
                # Inseriamo una nuova colonna per la classifica parziale di ogni indicatore
                finale.insert(loc=finale.columns.get_loc(colonna)+1,column="Punteggio_" + colonna,value=parziali.values()) 
            else:
                lista = finale.sort_values(by=[colonna],ascending=False)["Provincia"].tolist()
                
                for item in lista:
                    parziali[item]=score
                    classifica[item]+= score
                    score-=0.1
                finale.insert(loc=finale.columns.get_loc(colonna)+1,column="Punteggio_" + colonna,value=parziali.values()) #Inseriamo una nuova colonna con la classifica parziale
                 
                    
    for val in classifica.values(): #Tronchiamo i valori perchè in alcuni casi, a causa delle sottrazioni, venivano inserite diverse cifre deficimali: Dopo averli troncati li inseriamo in punteggi
        punteggi.append('%.1f'%val)
    
    finale["Indice_vivibilita"] = punteggi      
    
    coordinate(finale)
    
    finale.to_csv("Output_finale.csv",index=False,sep=",")
    
    
if __name__ == '__main__':
    merge()
    calcoloRank()
