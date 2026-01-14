import requests
import base64
import oracledb
import json
import unicodedata
from datetime import datetime

def trace (leMessage) :
    global globalFicTrace
    global DoTrace
    if DoTrace : 
        globalFicTrace.write(leMessage)
        globalFicTrace.write("\n")
    if DoDebug:
        globalFicDebug.write(leMessage)
        globalFicDebug.write("\n")   
    
def debug (leMessage):
    global DoDebug
    global globalFicDebug
    if DoDebug : 
        globalFicDebug.write(leMessage)
        globalFicDebug.write("\n")   

def trace2 (leMessage) :
    global globalFicTraceCsv
    global DoTrace
    if DoTrace and not (DoPostGp): 
        globalFicTraceCsv.write(leMessage)
        globalFicTraceCsv.write("\n")

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')  # Pour Python 2
    except NameError:
        pass  # unicode est par défaut sur Python 3
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
    return str(text)

def rapprocheTwoStringLarge (str1, str2) :
    try :
        lStr1 = str1.replace('None','') if not(str1 is None) else ''
        lStr2 = str2.replace('None','') if not(str2 is None) else ''
        if strip_accents (lStr1).upper ().replace (' ','') == strip_accents (lStr2).upper ().replace (' ','') :
            return (True)
        else :
            return (False)
    except :
        return (True)

def adapteTelephoneForGp (pChaine) :
    try :
        if isinstance(pChaine, int) :
            return (pChaine)
        else : 
            sChaine1 = pChaine.replace(' ','').replace('.','').replace('_','').replace('-','')  if not(pChaine is None) else '0'
            if sChaine1[0:1] == '0' :
                sChaine2 = sChaine1[1:]
            else :
                sChaine2 = sChaine1
            return int(sChaine2.strip())
    except :
        return 0

def rapprocheTwoSiret (str1, str2) :
    try :
        lStr1 = str1.replace('None','')[0:14] if not(str1 is None) else ''
        lStr2 = str2.replace('None','')[0:14] if not(str2 is None) else ''
        if strip_accents (lStr1).upper ().replace (' ','') == strip_accents (lStr2).upper ().replace (' ','') :
            return (True)
        else :
            return (False)
    except :
        return (True)

def rapprocheTelephone (num1, num2) :
    try :
        sNum1=str(num1 if not(num1 is None) else '0')
        sNum2=str(num2 if not(num2 is None) else '0')
        if sNum1.replace('0','') == '' and sNum2.replace('0','') == '' :
            return (True)    
        lNum1 = ''
        for car in sNum1 :
            if car == '0':
                pass
            else :
                lNum1 = lNum1 + car
        lNum2 = ''
        for car in sNum2 :
            if car == '0':
                pass
            else :
                lNum2 = lNum2 + car
        #lNum1 = str(sNum1 if sNum1[0] != '0' else sNum1[1:])
        #lNum2 = str(sNum2 if sNum2[0] != '0' else sNum2[1:])
        if lNum1.replace(' ','').replace('.','').replace('_','').replace('-','') == lNum2.replace(' ','').replace('.','').replace('_','').replace('-','') :
            return True
        else :
            return False
    except :
        return (True)

def initialiseParametreGlobalLRYE () :
    global globalUrlGP
    global globalUserPih
    global globalPwdPih
    global globalScsoPih
    global globalDsnPih
    global globalAcheteurGP
    global globalNbMaj
    global globalNbDel
    global globalNbIns
    global globalNbOk
    global globalDateCourte
    global DoTrace 
    global DoDebug
    global globalFicTrace
    global globalFicDebug
    global globalFicTraceCsv
    global DoPostGp  
    global globalCredentialGP
    DoTrace  = True
    DoDebug  = True
    DoPostGp = True

    globalAcheteurGP = 'LES RESIDENCES'
    ServeurGP    = 'NS3250347.gesprojet.com'
    UserApiGP    = 'JsonRes:Vc4#Sn7)Dw8!'
    PortGP       = '9548'
    ComplementGP = 'req_json?'
    httpGP       = 'https'
    globalUserPih  = 'LOGI'
    globalPwdPih   = 'SB'
    globalScsoPih  = 'OPI'
    globalDsnPih   = 'IG_PRODRYE'
    # globalDsnPih   = 'OnP_LR7891'
    globalUrlGP = httpGP +'://'+ ServeurGP +':'+ PortGP+'/'+ ComplementGP
    globalCredentialGP = base64.b64encode(UserApiGP.encode()).decode()
    oracledb.init_oracle_client(lib_dir=r"C:\Oracle\instantclient_21_13")
    globalNbMaj = 0
    globalNbDel = 0 
    globalNbIns = 0
    globalNbOk  = 0
    globalDateCourte = datetime.now().strftime("%d-%m-%y")
    NomFicTrace = 'C:\\Exploitation\\interfaceGpSaasPih4Saas\\Trace\\fournisseur_'+datetime.now().strftime("%d-%m-%Y-%H%M%S")+'.txt'
    NomFicDebug = 'C:\\Exploitation\\interfaceGpSaasPih4Saas\\Trace\\DebugFournisseur_'+datetime.now().strftime("%d-%m-%Y-%H%M%S")+'.txt'
    NomFicTraceCsv = 'C:\\Exploitation\\interfaceGpSaasPih4Saas\\Trace\\fournisseur_'+datetime.now().strftime("%d-%m-%Y-%H%M%S")+'.csv'
    if DoDebug : 
         globalFicDebug = open (NomFicDebug,'x')       
    if DoTrace : 
        globalFicTrace = open (NomFicTrace,'x')
    if DoTrace and not (DoPostGp):
        globalFicTraceCsv = open (NomFicTraceCsv,'x')
        trace2 (f'Action;Nom_Table;Raison_sociale;Numero_Rue;Code_et_ville;Telephone;Telecopie;Cloturer_le_tiers;Activite;BP_ZI_Lieu_dit;\
Email;Forme_juridique;Pays;Champ_libre_1;Champ_libre_2;Champ_libre_3;Commentaires;Imputation;Siret;APE;Numero_TVA;Rib_nom_banque;Iban;BIC;') 

def initialiseConnexionBasePih () :
    global globalConnexionPih
    global globalUserPih
    global globalPwdPih
    global globalScsoPih
    global globalDsnPih
    trace ('initialiseConnexionBasePih : Entree')
    try :
        globalConnexionPih = oracledb.connect( user=globalUserPih, password=globalPwdPih, dsn=globalDsnPih)
        trace ('initialiseConnexionBasePih : Base de donnee PIH > Disponible')
        return (True)
    except :
        trace ('initialiseConnexionBasePih : Base de donnee PIH > INDISPONIBLE')
        return (False)

def closeConnexionBasePih () :
    debug ('closeConnexionBasePih :Entree')
    global globalConnexionPih
    try :
        globalConnexionPih.close() 
        del (globalConnexionPih)
        debug ('closeConnexionBasePih :close = OK')
    except :
        debug ('closeConnexionBasePih : Exception')
        pass #La connexion était déjà fermée par perte de connexion ..

def cursorOracle_oneRowBindDict (laRequete, leDicoParam) :
    global globalConnexionPih
    cursorOracle = globalConnexionPih.cursor()
    locDon = cursorOracle.execute(laRequete,leDicoParam)
    columns = [col[0] for col in cursorOracle.description]
    cursorOracle.rowfactory = lambda *args: dict(zip(columns, args))
    resultat = cursorOracle.fetchone()
    cursorOracle.close()
    return (resultat)

def cursorOracle_multipleRowBindDict(laRequete,leDicoParam):
    global globalConnexionPih
    cursorOracle = globalConnexionPih.cursor()
    locDon = cursorOracle.execute(laRequete, leDicoParam)
    columns = [col[0] for col in cursorOracle.description]
    cursorOracle.rowfactory = lambda *args: dict(zip(columns, args))
    resultat = cursorOracle.fetchall()
    cursorOracle.close()
    return (resultat)  
          
def requeteGetGP (pComplementRequete) :
    try :
        debug ('requeteGetGP : Entree')
        #debug (f'>Complement de route = {pComplementRequete}')
        global globalUrlGP
        localPayLoad = []
        localHeader  = {"Authorization": f"Basic {globalCredentialGP}"}
        localUrl=globalUrlGP+pComplementRequete
        response=requests.request ('GET', url=localUrl, headers = localHeader, data = localPayLoad)
        if response and response.status_code in (200,201) :
            return (response)
        else :
            return (None)
    except :
        trace ('requeteGetGP : Erreur inatendue')
        return (None)

def requetePostGPReel (pAction, donneeGpDictionnaire) :
    try :
        global globalUrlGP
        global globalNbMaj
        global globalNbDel
        global globalNbIns
        #debug ('-----------------------------------------------------------------------')
        debug ('Entree dans requetePostGPReel')
        if  pAction == 'DESACTIVE' :
            globalNbDel += 1
            localNomTable = donneeGpDictionnaire[0]["Nom_Table"]
            localValeurId = donneeGpDictionnaire[0]["Valeur_ID"] 
        elif pAction == 'MAJ' :
            globalNbMaj += 1
            localNomTable = donneeGpDictionnaire[0]["Nom_Table"]
            localValeurId = donneeGpDictionnaire[0]["Valeur_ID"] 
        elif pAction == 'INS' :
            globalNbIns += 1
            localNomTable = donneeGpDictionnaire[0]["Nom_Table"]
            localValeurId = 0
        #debug (f'Prevu : {pAction}:{localNomTable}/id={localValeurId}')
      
        localUrl=f'{globalUrlGP}=null'
        #debug ('--------')
        #debug (f"Reel {localUrl} : {donneeGpDictionnaire}")
        payload = json.dumps (donneeGpDictionnaire)
        headers = {'Content-Type':'application/json',
                   'Authorization': f'Basic {globalCredentialGP}'}
        response=requests.request ("POST",url=localUrl,headers=headers,data=payload)
        #debug (f'reponse = {response}')
        #debug (f'statut = {response.status_code}')
        #debug (f'Text={response.text}')
        if response and response.status_code in (200,201) :
            trace ('requetePostGPReel : Retour = OK')
        else :
            trace('requetePostGPReel : Retour en erreur')
    except Exception as e:
        trace ('requetePostGPReel : Valeur renvoyé en erreur !!!{e}')

def requetePostGPDebug (pAction, donneeGpDictionnaire) :
    try :
        global globalUrlGP
        global globalNbMaj
        global globalNbDel
        global globalNbIns
        if  pAction == 'DESACTIVE' :
            globalNbDel += 1
            localNomTable = donneeGpDictionnaire[0]["Nom_Table"]
            localValeurId = donneeGpDictionnaire[0]["Valeur_ID"] 
        elif pAction == 'MAJ' :
            globalNbDel += 1
            localNomTable = donneeGpDictionnaire[0]["Nom_Table"]
            localValeurId = donneeGpDictionnaire[0]["Valeur_ID"] 
        elif pAction == 'INS' :
            globalNbIns += 1
            localNomTable = donneeGpDictionnaire[0]["Nom_Table"]
            localValeurId = 0
        jsonArgument = json.dumps(donneeGpDictionnaire)
        payload = json.dumps (donneeGpDictionnaire)
        headers = {'Content-Type':'application/json',
                   'Authorization': f'Basic {globalCredentialGP}'}
        localUrl=f'{globalUrlGP}=null'
        debug ('--------')
        debug (f"{pAction} : {donneeGpDictionnaire}")
        debug (f"ROUTE POST = {localUrl}")
        ligneFournisseur = (
    f"{pAction};{donneeGpDictionnaire[0]['Nom_Table']};"
    f"{donneeGpDictionnaire[0]['Raison_sociale']};"
    f"{donneeGpDictionnaire[0]['Numero_Rue']};"
    f"{donneeGpDictionnaire[0]['Code_et_ville']};"
    f"{donneeGpDictionnaire[0]['Telephone']};"
    f"{donneeGpDictionnaire[0]['Telecopie']};"
    f"{donneeGpDictionnaire[0]['Cloturer_le_tiers']};"
    f"{donneeGpDictionnaire[0]['Activite']};"
    f"{donneeGpDictionnaire[0]['BP_ZI_Lieu_dit']};"
    f"{donneeGpDictionnaire[0]['Email']};"
    f"{donneeGpDictionnaire[0]['Forme_juridique']};"
    f"{donneeGpDictionnaire[0]['Pays']};"
    f"{donneeGpDictionnaire[0]['Champ_libre_1']};"
    f"{donneeGpDictionnaire[0]['Champ_libre_2']};"
    f"{donneeGpDictionnaire[0]['Champ_libre_3']};"
    f"{donneeGpDictionnaire[0]['Commentaires']};"
    f"{donneeGpDictionnaire[0]['Imputation']};"
    f"{donneeGpDictionnaire[0]['Siret']};"
    f"{donneeGpDictionnaire[0]['APE']};"
    f"{donneeGpDictionnaire[0]['Numero_TVA']};"
    f"{donneeGpDictionnaire[0]['Rib_nom_banque']};"
    f"{donneeGpDictionnaire[0]['Iban']};"
    f"{donneeGpDictionnaire[0]['BIC']};"
)
        trace2 (ligneFournisseur) 
    except Exception as e:
         trace (f'requetePostGPDebug : En erreur !!!{e}')

def requetePostGP (pAction, donneeGpDictionnaire) :
    debug ('requetePostGP:Entree')
    donneeGpDictionnaire[0]['Telephone'] = adapteTelephoneForGp (donneeGpDictionnaire[0]['Telephone'])
    donneeGpDictionnaire[0]['Telecopie'] = adapteTelephoneForGp (donneeGpDictionnaire[0]['Telecopie'])
    if DoPostGp :
        requetePostGPReel (pAction, donneeGpDictionnaire) 
    else : 
        requetePostGPDebug (pAction, donneeGpDictionnaire)

def desactiveAdressGP (dicoAdrGP) :
    debug ('desactiveAdressGP : Entree')
    dicoAdrGP["Cloturer_le_tiers"] = True
    requetePostGP('DESACTIVE', [dicoAdrGP])

def desactiveRibGP (dicoAdrGP) :
    debug ('desactiveRibGP : Entree')
    dicoAdrGP["Rib_nom_banque"] = dicoAdrGP["Rib_nom_banque"]+'(inactif)'
    requetePostGP('DESACTIVE', [dicoAdrGP])   
    
def majAdresseGp (dicoAdrGP,dicoAdrPIH):
    debug ('majAdresseGp')
    dicoAdrGP["Champ_libre_1"]   = dicoAdrPIH ["FNFO"]
    dicoAdrGP["Champ_libre_2"]   = dicoAdrPIH ["SCSO"]
    dicoAdrGP["Champ_libre_3"]   = dicoAdrPIH ["SLSO"]
    dicoAdrGP["Telephone"]       = dicoAdrPIH ["TEL"] if dicoAdrPIH ["TEL"] != '' else 0
    dicoAdrGP["Telecopie"]       = dicoAdrPIH ["FAX"] if dicoAdrPIH ["FAX"] != '' else 0
    dicoAdrGP["Activite"]        = dicoAdrPIH ["ACTIVITE"]
    dicoAdrGP["BP_ZI_Lieu_dit"]  = dicoAdrPIH ["BP_ZI_LIEU_DIT"]
    dicoAdrGP["Pays"]            = dicoAdrPIH ["PAYS"]
    dicoAdrGP["Email"]           = dicoAdrPIH ["EMAIL"]
    dicoAdrGP["Forme_juridique"] = dicoAdrPIH ["FORME_JURIDIQUE"]
    dicoAdrGP["Siret"]           = dicoAdrPIH ["SIRET"]
    dicoAdrGP["APE"]             = dicoAdrPIH ["APE"]
    dicoAdrGP["Numero_TVA"]      = dicoAdrPIH ["NUM_TVA"]
    requetePostGP('MAJ',[dicoAdrGP])

def majRibGp (dicoRibGP,dicoRibPIH):
    debug ('majRibGp :Entree')
    dicoRibGP["Champ_libre_1"] = dicoRibPIH["FNFO"]
    dicoRibGP["Champ_libre_2"] = dicoRibPIH["SCSO"]
    dicoRibGP["Champ_libre_3"] = dicoRibPIH["SLSO"]
    dicoRibGP["BIC"]           = dicoRibPIH["BIC"] 
    requetePostGP('MAJ', [dicoRibGP])

def creationAdrGpVide (leDicoAdrGp, leNomFou, leCodeFou) :
    global globalAcheteurGP
    global globalScsoPih
    global globalDateCourte
    debug ('creationAdrGpVide :Entree')
    leDicoAdrGp["Nom_Table"]           = 'Adresses'
    leDicoAdrGp["Valeur_ID"]           = 0
    leDicoAdrGp["Raison_sociale"]      = leNomFou+' ( F'+str(leCodeFou)+' )'
    leDicoAdrGp["Numero_Rue"]          = '' 
    leDicoAdrGp["Code_et_ville"]       = ''
    leDicoAdrGp["Telephone"]           = 0
    leDicoAdrGp["Telecopie"]           = 0
    leDicoAdrGp["Cloturer_le_tiers"]   = False 
    leDicoAdrGp["Activite"]            = ''
    leDicoAdrGp["BP_ZI_Lieu_dit"]      = ''
    leDicoAdrGp["Pays"]                = ''
    leDicoAdrGp["Champ_libre_1"]       = leNomFou
    leDicoAdrGp["Champ_libre_2"]       = globalScsoPih
    leDicoAdrGp["Champ_libre_3"]       = globalAcheteurGP
    leDicoAdrGp["Champ_libre_4"]       = ''
    leDicoAdrGp["Commentaires"]        = ''
    leDicoAdrGp["Imputation"]          = 'F'+str(leCodeFou)
    leDicoAdrGp["Rib_nom_banque"]      = ''
    leDicoAdrGp["Rib_numero_banque"]   = ''
    leDicoAdrGp["Rib_numero_guichet"]  = ''
    leDicoAdrGp["Rib_numero_compte"]   = ''
    leDicoAdrGp["Rib_cle"]             = ''
    leDicoAdrGp["Export_compta"]       = True
    leDicoAdrGp["Email"]               = ''
    leDicoAdrGp["Forme_juridique"]     = ''
    leDicoAdrGp["Iban"]                = ''
    leDicoAdrGp["BIC"]                 = ''
    leDicoAdrGp["Siret"]               = ''
    leDicoAdrGp["Capital"]             = ''
    leDicoAdrGp["Delai_de_paiement"]   = ''
    leDicoAdrGp["Inclus_DADS"]         = False 
    leDicoAdrGp["APE"]                 = ''
    leDicoAdrGp["Numero_TVA"]          = ''
    leDicoAdrGp["Site_internet"]       = ''
    leDicoAdrGp["Adresse_complete"]    = ''
    leDicoAdrGp["Suivi"]               = globalDateCourte
    leDicoAdrGp["A_interfacer"]        = False
    leDicoAdrGp["Taux_escompte"]       = 0

def creationAdrGpFromPih (fourPIH, adrPIH) :
    debug ('creationAdrGpFromPih : Entree')
    dicoAdrGP = dict ()
    creationAdrGpVide (dicoAdrGP, fourPIH["FNFO"], fourPIH["FCFO"]) 
    dicoAdrGP["Rib_nom_banque"]      = '(inactif)'
    dicoAdrGP["Champ_libre_4"]       = f'F{fourPIH["FCFO"]}O'
    dicoAdrGP["Numero_Rue"]          = adrPIH ["ADR1"]
    dicoAdrGP["Code_et_ville"]       = adrPIH["CP_VILLE"]
    dicoAdrGP["BP_ZI_Lieu_dit"]      = adrPIH["BP_ZI_LIEU_DIT"]
    dicoAdrGP["Pays"]                = adrPIH["PAYS"]
    dicoAdrGP["Telephone"]           = adrPIH ["TEL"] if not (adrPIH ["TEL"] is None) else 0
    dicoAdrGP["Telecopie"]           = adrPIH ["FAX"] if not (adrPIH ["FAX"] is None) else 0
    dicoAdrGP["Cloturer_le_tiers"]   = False 
    dicoAdrGP["Activite"]            = fourPIH["ACTIVITE"]
    dicoAdrGP["Email"]               = adrPIH["EMAIL"] if not (adrPIH ["EMAIL"] is None) else ''
    dicoAdrGP["Forme_juridique"]     = fourPIH["FORME_JURIDIQUE"] if not (fourPIH ["FORME_JURIDIQUE"] is None) else ''
    dicoAdrGP["Siret"]               = adrPIH["SIRET"] if not (adrPIH ["SIRET"] is None) else ''
    dicoAdrGP["APE"]                 = fourPIH["APE"] if not (fourPIH ["APE"] is None) else ''
    dicoAdrGP["Numero_TVA"]          = fourPIH["NUMERO_TVA"] if not (fourPIH ["NUMERO_TVA"] is None) else ''
    requetePostGP('INS', [dicoAdrGP])
    del (dicoAdrGP)
 
def creationRibGpFromPih (fourPIH, ribPIH):
    debug ('creationRibGpFromPih : Entree')
    dicoRibGP = dict ()
    creationAdrGpVide (dicoRibGP, fourPIH["FNFO"], fourPIH["FCFO"])  
    dicoRibGP["Iban"]                = str(ribPIH["IBAN"])
    dicoRibGP["BIC"]                 = str(ribPIH["BIC"])
    dicoRibGP["Rib_nom_banque"]      = str(ribPIH["NTDOMB"])+' '+str(ribPIH["IBAN"])
    dicoRibGP["Cloturer_le_tiers"]   = True
    dicoRibGP["Activite"]            = 'DIVERS'
    dicoRibGP["Pays"]                = 'FRANCE'
    dicoRibGP["Champ_libre_4"]       = f'F{fourPIH["FCFO"]}/{ribPIH["IBAN"]}/O'
    requetePostGP('INS', [dicoRibGP])
    del (dicoRibGP)
                                    
def trouveAdrPihInGP (dicFouPih, dicAdrPih, listeAdrGP) :
    debug ('trouveAdrPihInGP : Entree')
    lEcart = ''
    for adrGp in listeAdrGP :
        lEcart = 'GP:ChampLibre1 / PIH:FNFO'
        if (rapprocheTwoStringLarge (adrGp["Champ_libre_1"], dicFouPih ["FNFO"])) :
            lEcart = 'GP:ChampLibre2 / PIH:SCSO'
            if (rapprocheTwoStringLarge (adrGp["Champ_libre_2"], dicFouPih ["SCSO"])) :
                lEcart = 'GP:Telephone / PIH:Tel'
                if (rapprocheTelephone (adrGp["Telephone"], dicAdrPih ["TEL"])) :
                    lEcart = 'GP: Telecopie / PIH: '
                    if (rapprocheTelephone (adrGp["Telecopie"], dicAdrPih ["FAX"])) :
                        lEcart = 'GP:Activite / PIH: ACTIVITE'
                        if (rapprocheTwoStringLarge (adrGp["Activite"], dicFouPih ["ACTIVITE"])) :
                            lEcart = 'GP: / PIH: '
                            if (rapprocheTwoStringLarge (adrGp["BP_ZI_Lieu_dit"], dicAdrPih ["BP_ZI_LIEU_DIT"])) :
                                lEcart = 'GP:BP_ZI_Lieu_dit / PIH:PAYS '
                                if (rapprocheTwoStringLarge (adrGp["Pays"], dicAdrPih ["PAYS"])) :
                                    lEcart = 'GP: Email/ PIH: EMAIL'
                                    if (rapprocheTwoStringLarge (adrGp["Email"], dicAdrPih ["EMAIL"])) :
                                        lEcart = 'GP:Forme_juridique / PIH: FORME_JURIDIQUE'
                                        if (rapprocheTwoStringLarge (adrGp["Forme_juridique"], dicFouPih ["FORME_JURIDIQUE"])) :
                                            lEcart = 'GP:Siret / PIH: SIRET'
                                            if (rapprocheTwoSiret (adrGp["Siret"], dicAdrPih ["SIRET"])) :
                                                lEcart = 'GP:APE / PIH: APE'
                                                if (rapprocheTwoStringLarge (adrGp["APE"], dicFouPih ["APE"])) :
                                                    lEcart = 'GP: Numero_TVA/ PIH:NUMERO_TVA '
                                                    if (rapprocheTwoStringLarge (adrGp["Numero_TVA"], dicFouPih ["NUMERO_TVA"])) :
                                                        lEcart = 'Trouve'
                                                        debug ('trouveAdrPihInGP : Trouvé > Sortie')
                                                        return (True)  # Sortie violente de la boucle mais gérée par Python ;->
    debug (f'trouveAdrPihInGP : Pas trouvé, écart sur  {lEcart}')
    debug (f'trouveAdrPihInGP : listeAdrGP={listeAdrGP}')
    debug (f'trouveAdrPihInGP : dicAdrPih={dicAdrPih}')
    debug (f'trouveAdrPihInGP : dicFouPih={dicFouPih}')
    debug ('trouveAdrPihInGP : Sortie')
    return (False)

def trouveRibPihInGP (dicFouPih, ribPIH, listeRibGP) :
    debug ('trouveRibPihInGP : Entree')
    #debug(f'trouveRibPihInGP : {dicFouPih} / {ribPIH} / {listeRibGP}')
    lEcart = ''
    for ribGp in listeRibGP :
        lEcart = 'Gp :Champ_libre_1 / PIH : FNFO'
        if (rapprocheTwoStringLarge (ribGp["Champ_libre_1"], dicFouPih ["FNFO"])) :
            lEcart = 'Gp : Champ_libre_2/ PIH : SCSO'
            if (rapprocheTwoStringLarge (ribGp["Champ_libre_2"], dicFouPih ["SCSO"])) :
                lEcart = 'Gp : Champ_libre_3/ PIH : SLSO'
                if (rapprocheTwoStringLarge (ribGp["Champ_libre_3"], dicFouPih ["SLSO"])) :
                    lEcart = 'Gp :Rib_nom_banque / PIH :NTDOMB '
                    if (1==1): # (rapprocheTwoStringLarge (ribGp["Rib_nom_banque"], ribPIH ["NTDOMB"])) :
                        lEcart = 'Gp : Iban/ PIH : IBAN'
                        if (rapprocheTwoStringLarge (ribGp["Iban"], ribPIH ["IBAN"])) :
                            lEcart = 'Gp : BIC / PIH : BIC '
                            if (rapprocheTwoStringLarge (ribGp["BIC"], ribPIH ["BIC"])) :
                               lEcart = 'Trouvé'
                               debug ('trouveRibPihInGP : Trouvé > Sortie')
                               return (True)  # Sortie violente de la boucle mais gérée par Python ;->
    debug (f'trouveRibPihInGP : Pas trouvé, ecart sur {lEcart}')
    debug (f'trouveRibPihInGP : {dicFouPih} ')
    debug (f'trouveRibPihInGP : {ribPIH} ')
    debug (f'trouveRibPihInGP : {listeRibGP} ')
    debug ('trouveRibPihInGP : Sortie ')
    return (False)

# laRefFouPIH doit se présenter sous la forme F+FCFO
# Attention au code société....
def ConstruitListeGpOneFou (laRefFouPIH) :
    debug ('ConstruitListeGpOneFou  : Entree')
    dicoFouGP = dict ()
    listeAdr = []
    listeRib = []
    dicoFouGP["Adresse"] = listeAdr 
    dicoFouGP["Rib"] = listeRib
    lArgument = f'table=Adresses&champ=adresses.Imputation&val={laRefFouPIH}'
    leTest = requeteGetGP (lArgument)
    if (leTest is None) :
        return dicoFouGP 
    if (len(leTest.text) == 0 ) :
        return (dicoFouGP)
    leJsonTemp = json.loads (leTest.text)
    del (leTest)
    for item in leJsonTemp : 
        locDone = False
        try :
            if item["Champ_libre_3"] == globalAcheteurGP :
                #if item['Iban'] == "" and item["Adresse_ID"] < 0 and not(item["Cloturer_le_tiers"]) and item["Rib_nom_banque"][-9:]=='(inactif)' :
                if item['Iban'] == "" and not(item["Cloturer_le_tiers"]) and item["Rib_nom_banque"][-9:]=='(inactif)' :
                    locDone = True
                    listeAdr.append (item) 
        except : 
            #probablement que le rib_nom_banque est plus court que 9 ....
            debug ('ConstruitListeGpOneFou : Erreur passee sur détermination ligne adresse')
            pass 
        if not(locDone) : 
            try :
                if item["Champ_libre_3"] == globalAcheteurGP and item["Imputation"][0] == 'F' :
                    #Determination du type de ligne GP :
                    #if not(item['Iban'] == "") and item["Adresse_ID"] < 0 and item["Cloturer_le_tiers"] : 
                    if not(item['Iban'] == "") and item["Cloturer_le_tiers"] : 
                        if len(item["Rib_nom_banque"]) > 2 :
                            locDone = True
                            if len(item["Rib_nom_banque"]) < 9 : ## Sans le && du C ...
                                locDone = True
                            else :
                                if (item["Rib_nom_banque"][-9:]) =='(inactif)' :
                                    locDone = False          
                                else :
                                    locDone = True 
                        else :
                            locDone = False
                    else :
                        locDone = False
                    if locDone : 
                        listeRib.append (item)
            except : 
                debug ('ConstruitListeGpOneFou : Erreur passee sur détermination ligne rib')
                pass
    del leJsonTemp
    return (dicoFouGP)

def completeDonneesGesprojetDepuisPIH ():
    global globalConnexionPih
    debug ('======================================================================================================================================')
    debug ('completeDonneesGesprojetDepuisPIH : Entree')
    debug ('======================================================================================================================================')
    cursorFouPih = globalConnexionPih.cursor()
    cursorFouPih.execute(f"select f.FCFO , FNFO||' ( F '||to_char(f.FCFO)||' )' ID, f.FNFO, f.FAPE APE, f.ID_FISC NUMERO_TVA, 'F'||to_char(F.FCFO) ID_GP,\
                                           s.SLSO, s.SCSO, j.JULIB FORME_JURIDIQUE, nvl(n.nflibnf,'DIVERS') ACTIVITE \
                                      from kformjur j, knatfou n, ksociet s, kfourni f \
                                     where f.scso = '{globalScsoPih}' and f.valid = 'O' and s.scso = f.scso and j.juc (+)= f.juc and n.nfcodnf(+)= f.nfcodnf")
    columns1 = [col[0] for col in cursorFouPih.description]
    cursorFouPih.rowfactory = lambda *args: dict(zip(columns1, args))
    while True :
        fourPIH = cursorFouPih.fetchone()
        if fourPIH is None : 
            break
        else :
            donGP = ConstruitListeGpOneFou (fourPIH["ID_GP"])
            cursorAdressePih = globalConnexionPih.cursor ()
            cursorAdressePih.execute (f"select distinct a.adr1 ADR1, a.cp||' '||a.ville CP_VILLE, replace(a.tel,'.','') TEL, replace (a.fax,'.','') FAX, \
                                                        a.adr2 BP_ZI_LIEU_DIT, nvl(a.pays,'FRANCE') PAYS, a.mail EMAIL, a.asiret SIRET \
                                                   from kfouadr a where a.scso = '{fourPIH["SCSO"]}' and a.factier = {fourPIH["FCFO"]} and a.fattier = 'F'")
            columns2 = [col[0] for col in cursorAdressePih.description]
            cursorAdressePih.rowfactory = lambda *args: dict(zip(columns2, args)) 
            while True :
                adrPIH = cursorAdressePih.fetchone ()
                if adrPIH is None :
                   break
                else : 
                    if not(trouveAdrPihInGP (fourPIH, adrPIH,donGP["Adresse"])) :
                        creationAdrGpFromPih (fourPIH, adrPIH)
                    del(adrPIH)
            cursorAdressePih.close ()
            del (cursorAdressePih)
            cursorRibPih = globalConnexionPih.cursor ()
            cursorRibPih.execute (f"select distinct bic BIC, iban IBAN, ntdomb NTDOMB from kntsfou where scso = '{fourPIH["SCSO"]}' and fcfo = {fourPIH["FCFO"]} and actif = 'O' and length(replace(iban,' '))>0 ")
            columns3 = [col[0] for col in cursorRibPih.description]
            cursorRibPih.rowfactory = lambda *args: dict(zip(columns3, args)) 
            while True : 
                ribPIH = cursorRibPih.fetchone ()
                if ribPIH is None :
                    break 
                else :
                    if not(trouveRibPihInGP (fourPIH, ribPIH, donGP["Rib"])) :
                        creationRibGpFromPih (fourPIH, ribPIH)
                    del (ribPIH)
            cursorRibPih.close ()
            del (cursorRibPih)
            del(donGP)
    cursorFouPih.close ()
    del(cursorFouPih)

def rapprocheAdrGpPih (dicoAdrGP,listeDicoAdrPIH):
    debug ('rapprocheAdrGpPih : Entree')
    lEcart = ''
    for adrPih in listeDicoAdrPIH :
        lEcart = f'rapprocheAdrGpPih :Champ_libre_1 / FNFO '
        if (rapprocheTwoStringLarge (dicoAdrGP["Champ_libre_1"], adrPih ["FNFO"])) :
            lEcart = f'rapprocheAdrGpPih : Champ_libre_2 / SCSO'
            if (rapprocheTwoStringLarge (dicoAdrGP["Champ_libre_2"], adrPih ["SCSO"])) :
                lEcart = f'rapprocheAdrGpPih : Telephone / TEL'
                if (rapprocheTelephone (dicoAdrGP["Telephone"], adrPih ["TEL"])) :
                    lEcart = f'rapprocheAdrGpPih : Telecopie / FAX'
                    if (rapprocheTelephone (dicoAdrGP["Telecopie"], adrPih ["FAX"])) :
                        lEcart = f'rapprocheAdrGpPih : Activite / Activite'
                        if (rapprocheTwoStringLarge (dicoAdrGP["Activite"], adrPih ["ACTIVITE"])) :
                            lEcart = f'rapprocheAdrGpPih : BP_ZI_Lieu_dit/BP_ZI_Lieu_dit '
                            if (rapprocheTwoStringLarge (dicoAdrGP["BP_ZI_Lieu_dit"], adrPih ["BP_ZI_LIEU_DIT"])) :
                                lEcart = f'rapprocheAdrGpPih : Pays/Pays'
                                if (rapprocheTwoStringLarge (dicoAdrGP["Pays"], adrPih ["PAYS"])) :
                                    lEcart = f'rapprocheAdrGpPih : Email/Email'
                                    if (rapprocheTwoStringLarge (dicoAdrGP["Email"], adrPih ["EMAIL"])) :
                                        lEcart = f'rapprocheAdrGpPih : Forme_juridique/Forme_juridique'
                                        if (rapprocheTwoStringLarge (dicoAdrGP["Forme_juridique"], adrPih ["FORME_JURIDIQUE"])) :
                                            lEcart = f'rapprocheAdrGpPih : Siret/Siret'
                                            if (rapprocheTwoSiret (dicoAdrGP["Siret"], adrPih ["SIRET"])) :
                                                lEcart = f'rapprocheAdrGpPih : APE/APE'
                                                if (rapprocheTwoStringLarge (dicoAdrGP["APE"], adrPih ["APE"])) :
                                                    lEcart = f'rapprocheAdrGpPih : Numero_TVA/Numero_TVA'
                                                    if (rapprocheTwoStringLarge (dicoAdrGP["Numero_TVA"], adrPih ["NUMERO_TVA"])) :
                                                        lEcart = ''
                                                        debug('rapprocheAdrGpPih : Trouve > sortie')
                                                        return (True)  # Sortie violente de la boucle mais gérée par Python ;->
    debug (f'rapprocheAdrGpPih : Ecart sur {lEcart}')
    debug (f'rapprocheAdrGpPih : dicoAdrGP = {dicoAdrGP}')
    debug (f'rapprocheAdrGpPih : listeDicoAdrPIH = {listeDicoAdrPIH}')
    debug ('rapprocheAdrGpPih : Sortie ')
    return (False)

def rapprocheRibGpPih (dicoRibGP,listeDicoRibPIH):
    debug ('rapprocheRibGpPih : Entree')
    lEcart = ''
    for rib in listeDicoRibPIH :
        lEcart = 'rapprocheRibGpPih : Champ_libre_1 / FNFO'
        if rapprocheTwoStringLarge(dicoRibGP["Champ_libre_1"],rib["FNFO"]) :
            lEcart = 'rapprocheRibGpPih :Champ_libre_2 / SCSO '
            if rapprocheTwoStringLarge(dicoRibGP["Champ_libre_2"] , rib["SCSO"] ):
                lEcart = 'rapprocheRibGpPih : Champ_libre_3 / SLSO'
                if rapprocheTwoStringLarge(dicoRibGP["Champ_libre_3"] , rib["SLSO"] ):
                    lEcart = 'rapprocheRibGpPih : BIC / BIC '
                    if rapprocheTwoStringLarge(dicoRibGP["BIC"], rib["BIC"]) :
                        lEcart = 'rapprocheRibGpPih : Iban / IBAN'
                        if rapprocheTwoStringLarge(dicoRibGP["Iban"],rib["IBAN"] ) :
                            debug ('rapprocheRibGpPih : Trouvé > Sortie')
                            return (True) # Sortie violente de la boucle mais gérée par Python ;->
    debug (f'rapprocheRibGpPih : Ecart sur {lEcart}')
    debug (f'rapprocheRibGpPih : dicoRibGp = {dicoRibGP}')
    debug (f'rapprocheRibGpPih : listeDicoRibPIH = {listeDicoRibPIH}')
    debug ('rapprocheRibGpPih : Sortie')
    return (False)
     
def trouveAdressePIH (dicoAdrGP) :
    try :
        debug ('trouveAdressePIH : Entrée')
        dicoSql = dict(PSCSO = globalScsoPih, PFCFO=dicoAdrGP['Imputation'][1:], PNUMERORUE = dicoAdrGP['Numero_Rue'], PCPVILLE = dicoAdrGP['Code_et_ville'] )
        reqPih = f"SELECT nvl(f.fnfo,'')  FNFO, s.SCSO SCSO, s.SLSO SLSO, nvl(a.adr1,'')  ADR1, nvl(a.cp||' '||a.ville,'') CP_VILLE, nvl(replace (a.tel,'.',''),'') TEL, \
                        replace (a.fax,'.','') FAX ,  nvl(n.nflibnf,'DIVERS') ACTIVITE,   \
                        nvl(a.adr2,'') BP_ZI_LIEU_DIT      , nvl(a.pays,'FRANCE')  PAYS       ,  nvl(a.mail,'')  EMAIL, \
                        nvl(j.julib,'')  FORME_JURIDIQUE   ,  nvl(a.asiret,'')  SIRET  , \
                        nvl(f.fape,'')  APE, nvl(f.id_fisc,'')  NUM_TVA  , \
                        nvl(a.numadr,0)  NTNUM \
                        FROM ksociet s, knatfou n, kformjur j, kfouadr a, kfourni f  \
                        WHERE f.scso =  :PSCSO and f.fcfo = :PFCFO and a.scso = f.scso and a.fattier = 'F' and a.factier = f.fcfo \
                            and nvl(upper(replace(replace(replace(replace(a.adr1,'#'),' '),'-'),'_')),'#$__$#') = nvl(upper(replace(replace(replace(replace(:PNUMERORUE,'#'),' '),'-'),'_')),'#$__$#')  \
                            and nvl(upper(replace(replace(replace(replace(a.cp||a.ville, '#'),' '),'-'),'_')),'#$__$#')  = nvl(upper(replace(replace(replace(replace(:PCPVILLE,'#'),' '),'-'),'_')),'#$__$#')  \
                            and s.scso = f.scso \
                            and j.juc (+)= f.juc and n.nfcodnf (+)= f.nfcodnf \
                        ORDER BY nvl(a.numadr,0) desc"
        listeAdrPIH =  cursorOracle_multipleRowBindDict (reqPih, dicoSql)
        debug (f'trouveAdressePIH:Trouve ')
        if len(listeAdrPIH) == 0 :
            debug (f'trouveAdressePIH:Pas trouve')
            return None
        else :
            for adr in listeAdrPIH :
                for key, value in adr.items ():
                    if value is None :
                        adr[key]=''
            debug (f'trouveAdressePIH: Trouve')
            return (listeAdrPIH)
    except : 
        debug (f'trouveAdressePIH:Erreur inattendue')
        return (None)

def trouveRibPIH (dicoAdrGP) :
    try :
        debug ('trouveRibPIH : Entree')
        #debug(f'trouveRibPIH : codeFou = {dicoAdrGP['Imputation'][1:]} / IBAN={dicoAdrGP['Iban']}')
        dicoParam = dict (PSCSO = globalScsoPih, PCODEFOU = dicoAdrGP['Imputation'][1:] , PIBANFOU= dicoAdrGP['Iban'])
        reqPih = f"SELECT nvl(f.fnfo,'')  FNFO, s.SCSO SCSO, s.SLSO SLSO, a.bic BIC, a.iban  IBAN, a.ntdomb NTDOMB, \
                        nvl(a.ntnum,0)  NTNUM  \
                        FROM ksociet s, kntsfou a, kfourni f  \
                        WHERE f.scso =  :PSCSO and f.fcfo = :PCODEFOU and a.scso = f.scso and a.fcfo = f.fcfo and a.actif = 'O' and s.scso = :PSCSO \
                            and a.iban = :PIBANFOU \
                        ORDER BY nvl(a.ntnum,0) desc"
        listeRibPIH =  cursorOracle_multipleRowBindDict(reqPih,dicoParam)
        #debug(f'trouveRibPIH : trouve {listeRibPIH}')
        if len(listeRibPIH) == 0 :
            debug(f'trouveRibPIH : Pas trouve')
            return None
        else :
            for rib in listeRibPIH :
                for key, value in rib.items ():
                    if value is None :
                        rib[key]=''
            debug(f'trouveRibPIH : trouve')
            return (listeRibPIH)
    except : 
        debug(f'trouveRibPIH :Erreur inattendue')
        return (None)

# laRefFouPIH doit se présenter sous la forme F+FCFO
# Attention au code société....
def ExtraitInfoGpFou (laRefFouPIH):
    lArgument = f'table=Adresses&champ=adresses.Imputation&val={laRefFouPIH}'
    leTest = requeteGetGP (lArgument)
    if (leTest is None) :
        return ([])
    if (len(leTest.text) == 0 ) :
        return ([])
    else :    
        leJsonTemp = json.loads (leTest.text)
        del (leTest)
        listeDicoFournisseur = []
        for item in leJsonTemp :
            try : 
                if item["Champ_libre_3"] == globalAcheteurGP :
                    listeDicoFournisseur.append (item)
            except : #Problablement la clef n'existe pas ... tant pis
                pass 
        return (listeDicoFournisseur)

def rapprocheDonneesGesprojetAvecPIH () : #Detection des elements caducques sur GP ou a mettre à jour
    global globalNbOk
    debug ('======================================================================================================================================')
    debug ('rapprocheDonneesGesprojetAvecPIH : Entree')
    debug ('======================================================================================================================================')
    lArgument = "table=Adresses"
    #lArgument = f'table=Adresses&champ=adresses.Imputation&val=F17445'
    leTest = requeteGetGP (lArgument)
    if (leTest is None) :
        debug ('rapprocheDonneesGesprojetAvecPIH : Récupération de toute les adresses GP en échec')
    if (len(leTest.text) == 0 ) :
        debug ('rapprocheDonneesGesprojetAvecPIH : Récupération de toute les adresses GP aucune ligne !!')
    else :
        leJsonTemp = json.loads (leTest.text)
        del(leTest)
        for lgn in leJsonTemp :
            if lgn["Champ_libre_3"] == globalAcheteurGP and lgn["Imputation"][0] == 'F'  :
                #debug ('rapprocheDonneesGesprojetAvecPIH : Perimetre OK')
                #debug (f'rapprocheDonneesGesprojetAvecPIH : lgn = {lgn}')
                doSomething = False
                try :
                    if lgn['Iban'] == "" and not(lgn["Cloturer_le_tiers"]) and lgn["Rib_nom_banque"][-9:]=='(inactif)' :
                        debug ('rapprocheDonneesGesprojetAvecPIH : C est une adresse ')
                        listeAdressePIH = trouveAdressePIH (lgn)
                        if ( (listeAdressePIH is None) or (listeAdressePIH == []) ):
                            #debug (f'rapprocheDonneesGesprojetAvecPIH : desactiveAdressGP ({lgn})')
                            doSomething = True
                            desactiveAdressGP (lgn) 
                        else :
                            if not( rapprocheAdrGpPih (lgn, listeAdressePIH)) :
                                #debug (f'rapprocheDonneesGesprojetAvecPIH : majAdresseGp ({lgn})')
                                doSomething = True
                                majAdresseGp (lgn, listeAdressePIH[0]) #Le 0 est arbitraire, je favorise la dernière adresse saisie qui corresponde
                            else :
                                doSomething = True
                                #debug (f'rapprocheDonneesGesprojetAvecPIH : Adr identix  ({lgn})')
                                globalNbOk += 1
                        del(listeAdressePIH)
                except : 
                    pass  
                try :
                    #Dectection de l'acheteur
                    if not(lgn['Iban'] == "") and lgn["Cloturer_le_tiers"] : 
                        debug ('rapprocheDonneesGesprojetAvecPIH : C est un RIB ')
                        if len(lgn["Rib_nom_banque"]) > 2 :
                            doTheTest = True
                            if len(lgn["Rib_nom_banque"]) < 9 : ## Sans le && du C ...
                                doTheTest = True
                            else :
                                if (lgn["Rib_nom_banque"][-9:]) =='(inactif)' :
                                    doTheTest = False
                            if doTheTest :
                                #NB : trouveRibPIH cherche depuis l'iban, donc il n'est pas utile de le tester par la suite ....
                                listeRibPIH = trouveRibPIH (lgn)
                                if ((listeRibPIH is None) or (listeRibPIH == []))  :
                                    #debug (f'rapprocheDonneesGesprojetAvecPIH : desactiveRibGP ({lgn})')
                                    doSomething = True
                                    desactiveRibGP (lgn) 
                                else :
                                    if not( rapprocheRibGpPih (lgn, listeRibPIH)) :
                                        #debug (f'rapprocheDonneesGesprojetAvecPIH : majRibGp ({lgn})')
                                        doSomething = True
                                        majRibGp (lgn, listeRibPIH[0])
                                    else : 
                                        #debug (f'rapprocheDonneesGesprojetAvecPIH : RIB identix  ({lgn})')
                                        doSomething = True
                                        globalNbOk += 1
                                del (listeRibPIH)
                except : 
                    pass  
                               
def doIt ():
    global ListeAdresseGP
    global globalNbMaj
    global globalNbDel
    global globalNbIns
    global globalNbOk
    global DoTrace
    initialiseParametreGlobalLRYE ()
    trace ('Lancement global')
    if initialiseConnexionBasePih () :
        rapprocheDonneesGesprojetAvecPIH ()
        completeDonneesGesprojetDepuisPIH ()
    else :
        trace ('Base de données métier non disponible !!')
    trace ('Resumé :')
    trace (f'- Nombre de ligne rapprochee sans action =  {globalNbOk}')
    trace (f'- Nombre de ligne rapprochee avec MAJ    =  {globalNbMaj}')
    trace (f'- Nombre de ligne rapprochee avec SUP    =  {globalNbDel}')
    trace (f'- Nombre de ligne inseree                =  {globalNbIns}')
    if DoTrace :
        globalFicTrace.close ()
    if DoTrace and not (DoPostGp) :
        globalFicTraceCsv.close ()
    if DoDebug :
        globalFicDebug.close ()
    
if __name__ == "__main__":
    doIt()
