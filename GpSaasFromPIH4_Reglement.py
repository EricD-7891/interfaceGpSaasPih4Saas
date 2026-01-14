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

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')  # Pour Python 2
    except NameError:
        pass  # unicode est par défaut sur Python 3
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
    return str(text)

def initialiseParametreGlobal () :
    global globalUrlGP
    global globalCredentialGP
    global globalUserPih
    global globalPwdPih
    global globalScsoPih
    global globalDsnPih
    global globalAcheteurGP
    global globalDateCourte
    global DoTrace 
    global globalFicTrace    
    global globalNbCreeTheorique
    global globalNbParcouru
    global globalNbPostGp
    DoTrace = True
    
    globalNbCreeTheorique = 0
    globalNbParcouru      = 0
    globalNbPostGp        = 0

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
    globalDateCourte = datetime.now().strftime("%d-%m-%y")
    NomFicTrace = 'C:\\Exploitation\\interfaceGpSaasPih4Saas\\Trace\\reglements_'+datetime.now().strftime("%d-%m-%Y-%H%M%S")+'.txt'
    if DoTrace : 
        globalFicTrace = open (NomFicTrace,'x')
 
def initialiseConnexionBasePih () :
    global globalConnexionPih
    global globalUserPih
    global globalPwdPih
    global globalScsoPih
    global globalDsnPih
    trace ('initialiseConnexionBasePih : Entree')
    try :
        globalConnexionPih = oracledb.connect( user=globalUserPih, password=globalPwdPih, dsn=globalDsnPih)
        trace ('initialiseConnexionBasePih : Connexion = OK')
        return (True)
    except :
        trace ('initialiseConnexionBasePih : Connexion indisponible')
        return (False)

def closeConnexionBasePih () :
    global globalConnexionPih
    try :
        globalConnexionPih.close() 
        del (globalConnexionPih)
    except :
        pass #La connexion était déjà fermée par perte de connexion ..

def cursorOracle_oneRow(laRequete):
    global globalConnexionPih
    cursorOracle = globalConnexionPih.cursor()
    locDon = cursorOracle.execute(laRequete)
    columns = [col[0] for col in cursorOracle.description]
    cursorOracle.rowfactory = lambda *args: dict(zip(columns, args))
    resultat = cursorOracle.fetchone()
    cursorOracle.close()
    return (resultat)

def cursorOracle_multipleRow(laRequete):
    global globalConnexionPih
    cursorOracle = globalConnexionPih.cursor()
    locDon = cursorOracle.execute(laRequete)
    columns = [col[0] for col in cursorOracle.description]
    cursorOracle.rowfactory = lambda *args: dict(zip(columns, args))
    resultat = cursorOracle.fetchall()
    cursorOracle.close()
    return (resultat)    

def requeteGetGP (pComplementRequete) :
    try :
        global globalUrlGP
        #trace ('requeteGetGP : Entree')
        localPayLoad = []
        localHeader  = {"Authorization": f"Basic {globalCredentialGP}"}
        localUrl=globalUrlGP+pComplementRequete
        response=requests.request ('GET', url=localUrl, headers = localHeader, data = localPayLoad)
        if response and response.status_code in (200,201) :
            #trace ('requeteGetGP : Response Code = 200/201')
            return (response)
        else :
            trace ('requeteGetGP : Response Code <> 200/201 --> ANOMALIE')
            return (None)
    except :
        trace ('requeteGetGP : Erreur inatendue')
        return (None)

def requetePostGPReel (pAction, donneeGpDictionnaire) :
    try :
        global globalUrlGP
        global globalNbPostGp
        #trace ('requetePostGP : Entree')
        localUrl=f'{globalUrlGP}=null'
        #trace ('--------')
        #trace (f"{pAction} : {donneeGpDictionnaire}")
        #trace (f"ROUTE POST = {localUrl}")
        payload = json.dumps (donneeGpDictionnaire)
        headers = {'Content-Type':'application/json',
                   'Authorization': f'Basic {globalCredentialGP}'}
        response=requests.request ("POST",url=localUrl,headers=headers,data=payload)
        globalNbPostGp += 1
        if response and response.status_code in (200,201) :
            #trace ('requetePostGP : Response Code = 200/201')
            return (response)
        else :
            trace ('requetePostGP : Response Code <> 200/201 --> ANOMALIE')
            return (None)
    except :
        trace ('requetePostGP : Erreur inatendue')
        return (None)
    
def requetePostGPDebug (pAction, donneeGpDictionnaire) :
    try :
        global globalUrlGP
        global globalNbPostGp
        trace ('requetePostGP : Entree')
        localUrl=f'{globalUrlGP}=null'
        payload = json.dumps (donneeGpDictionnaire)
        headers = {'Content-Type':'application/json',
                   'Authorization': f'Basic {globalCredentialGP}'}
        trace ('--------')
        trace (f"{pAction} : {donneeGpDictionnaire}")
        trace (f"ROUTE POST = {localUrl}")
        trace (f'payload = {payload}')
        trace (f'headers = {headers}')
        globalNbPostGp += 1
    except :
        trace ('requetePostGP : Erreur inatendue')
        return (None)

def requetePostGP (pAction, donneeGpDictionnaire) :
    #requetePostGPDebug (pAction, donneeGpDictionnaire)
    ##if donneeGpDictionnaire[0]["Nom_Table"] == 'Decaissement' :
    ##     if donneeGpDictionnaire[0]["Code_facture"] == 395280 :
    ##         requetePostGPReel (pAction, donneeGpDictionnaire)
    requetePostGPReel (pAction, donneeGpDictionnaire)     

def testExistanceDecaissement (CodeFacture) :
    if (CodeFacture is None) :
        return(False) 
    else :
        try :
            lArgument = f'table=decaissement&champ=decaissement.Code_facture&val={CodeFacture}'
            leTest = requeteGetGP (lArgument)
            if leTest is None :
                return (False)
            else :
                if (leTest.text == '[]') :
                    return (False)
                else:
                    return (True)
        except :
            return (False)

# def testExistanceEncaissement (CodeRecette) :
#     if (CodeRecette is None) :
#         return(False) 
#     else :
#         try :
#             lArgument = f'table=encaissement&champ=encaissement.Code_recette&val={CodeRecette}'
#             leTest = requeteGetGP (lArgument)
#             if leTest is None :
#                 return (False)
#             else :
#                 if (leTest.text == '[]') :
#                     return (False)
#                 else:
#                     return (True)
#         except :
#             return (False)
        
def ListeProjet () :
    try :
        lArgument = f'table=projets&champ=projets.passation&val={globalAcheteurGP}&prop=Numero_contrat,Numero_operation'
        leTest = requeteGetGP (lArgument)
        if (leTest is None) :
            return ([])
        if (len(leTest.text) == 0 ) :
            return ([])
        else :
            leJsonTemp = json.loads (leTest.text)
            laListeOperation = {}
            for item in leJsonTemp :
                if not (item["Numero_contrat"] in laListeOperation):
                    laListeOperation.update ({item["Numero_contrat"]:item["Numero_operation"]})
            del (leJsonTemp)                
        return (laListeOperation)
    except :
        return ([])

# Ramene la liste des factures qui n'ont pas déjà fait l'objet d'un decaissement.
def ListeFactures (numeroOperation) :
    try :
        lArgument = f'table=factures&champ=factures.Numero_operation&val={numeroOperation}&prop=passation,code_facture,numero_operation,facture_ttc,contrepartie,reglee'
        leTest = requeteGetGP (lArgument)
        if (leTest is None) :
            return ({})
        if (len(leTest.text) == 0 ) :
            return ({})
        else :
            laListe = json.loads (leTest.text)
            leDicoFactures = {}
            for FactGp in laListe :
                if (         FactGp['Passation']== globalAcheteurGP  and FactGp["Contrepartie"][0:3] in ('401','404','402') 
                     and not(FactGp["Facture_TTC"] == 0)             and not(FactGp['Reglee']) ) :
                       if not (testExistanceDecaissement (FactGp["Code_facture"])) :
                           leDicoFactures[FactGp["Code_facture"]] = FactGp
            return (leDicoFactures)
    except :
        return ({})       

# def ListeRecettes (numeroOperation) :
#     try :
#         lArgument = f'table=recettes&champ=recettes.Numero_operation&val={numeroOperation}&prop=passation,code_recette,numero_operation,recette_ttc,contrepartie,reglee'
#         leTest = requeteGetGP (lArgument)
#         if (leTest is None) :
#             return ({})
#         if (len(leTest.text) == 0 ) :
#             return ({})
#         else :
#             laListe = json.loads (leTest.text)
#             leDicoRecette = {}
#             for RecGP in laListe :
#                  if (        RecGP['Passation']== globalAcheteurGP  and RecGP["Contrepartie"][0:4] in ('4411','4713','4672') 
#                      and not(RecGP["Recette_TTC"] == 0)            and not(RecGP['Reglee']) ) :
#                        if not (testExistanceDecaissement (RecGP["Code_recette"])) :
#                            leDicoRecette[RecGP["Code_recette"]] = RecGP 
#             return (leDicoRecette)
#     except :
#         return ({})  
        
def listePiecesPotentiellesPIH () : # Attention, l'order by a du sens !! A030 01
    requeteSqlPih = "select sum(nvl(a.brmt,0)*decode(a.regtyp,'F',1,-1)) mthtre, a.regtyp, to_char(a.fadpai,'YYYY-MM-DD') fadpai, a.mcmp, a.reglib, \
                            a.nopie, a.opcctr, a.opphas   from kregatt a  where a.scso = '"+globalScsoPih+ "' \
                    and a.opcctr is not null and a.opphas is not null and a.regval = 'O' and a.letdate > add_months (sysdate, -6) \
                    and a.nopie > 0 and a.faexe >= to_number(to_char(sysdate,'YYYY')) - 1 \
                    and exists (select 1 from ksbecr e, ksbecrl l \
                                 where l.brexe = a.faexe   and l.scso = a.scso     and l.brnpiec = a.nopie \
                                   and l.fatype = 'E'      and l.opcctr = a.opcctr and l.opphas = a.opphas \
                                   and e.scso = l.scso     and e.brexe = l.brexe   and e.pec   = l.pec \
                                   and e.brecr = l.brecr   and e.tjcod = a.ori_tjcod) \
                    group by a.regtyp, to_char(a.fadpai,'YYYY-MM-DD'), a.mcmp, a.reglib, a.nopie, a.opcctr, a.opphas \
                        order by a.opcctr, a.opphas"
    listeReglementPih = cursorOracle_multipleRow (requeteSqlPih)
    return (listeReglementPih)
        
def creationElementGp (laListeElemCreerGP) :
    dec = 0
    for newElement in laListeElemCreerGP :
        dec += 1
        apiGP = requetePostGP ('INS', [newElement])
    
def doIt ():
    global globalNbCreeTheorique
    global globalNbParcouru
    global globalFicTrace
    listeNewDecEncGesProjet = []
    initialiseParametreGlobal ()
    trace ('Lancement de doIt')
    globalNbParcouru      = 0
    globalNbCreeTheorique = 0
    if initialiseConnexionBasePih () :
        listePIH = listePiecesPotentiellesPIH ()
        oldOpcctr = 'SITAPA2SOU'
        oldOpphas = 'TKBOIR2LO'
        oldOnSenFou = 'PASDUWISKI'
        listeOperation = ListeProjet ()
        closeConnexionBasePih ()
        for piecePIH in listePIH :
            globalNbParcouru += 1
            if piecePIH ["OPCCTR"]+piecePIH["OPPHAS"] in listeOperation :
                if (oldOpcctr == piecePIH ["OPCCTR"] and oldOpphas == piecePIH ['OPPHAS']) :
                    pass 
                else : 
                    numeroOpGP=listeOperation[piecePIH ["OPCCTR"]+piecePIH["OPPHAS"]]
                    DicoFactureGP = ListeFactures (numeroOpGP) 
#                    DicoRecetteGP = ListeRecettes (numeroOpGP)
                    oldOpcctr = piecePIH ["OPCCTR"] 
                    oldOpphas = piecePIH ['OPPHAS']
                if  piecePIH["NOPIE"] in DicoFactureGP :
                    factGP = DicoFactureGP [piecePIH["NOPIE"]]
                    NewDecaissement =  {'Nom_Table': 'Decaissement', 
                                        'Valeur_ID': 0, 
                                        'Numero': 1, 
                                        'Decaissement_TTC': piecePIH['MTHTRE'], 
                                        'Date_decaissement': piecePIH['FADPAI'], 
                                        'Code_facture': factGP["Code_facture"], 
                                        'Numero_operation': factGP["Numero_operation"], 
                                        'Export_comptable': True, 
                                        'Date_export_comptable': piecePIH['FADPAI'], 
                                        'Type_de_reglement': 'Autre', 
                                        'Date_emission_decaissement': piecePIH['FADPAI'],
                                        'Reference_decaissement': strip_accents(piecePIH["REGLIB"]),
                                        'Export_Etebac': False, 
                                        'Date_de_saisie': piecePIH['FADPAI'],
                                        'Imputation_comptable': '0',
                                        'Journal': factGP["Code_facture"], 
                                        'Heure_export_comptable': 0, 
                                        'Heure_decaissement': 0, 
                                        'Cheque_Edite': False, 
                                        'Reimputation_remuneration': False, 
                                        'Commentaires': ''}
                    listeNewDecEncGesProjet.append (NewDecaissement)
                    globalNbCreeTheorique += 1
                    del (NewDecaissement)
                    del (factGP)
#                if  piecePIH["NOPIE"] in DicoRecetteGP :
#                    recGP = DicoRecetteGP[piecePIH["NOPIE"]]
#                    NewDecaissement =  {'Nom_Table': 'Encaissement',                                 
#                                        'Valeur_ID': 0,                                              
#                                        'Numero': 1,                                                    
#                                        'Encaissement_TTC': piecePIH['MTHTRE'],                      
#                                        'Date_encaissement': piecePIH['FADPAI'],                     
#                                        'Code_recette': recGP["Code_recette"],                       
#                                        'Numero_operation': recGP["Numero_operation"],               
#                                        'Export_comptable': True,                                    
#                                        'Date_export_comptable': piecePIH['FADPAI'],                 
#                                        'Reference_encaissement': strip_accents(piecePIH["REGLIB"]), 
#                                        'Date_de_saisie': piecePIH['FADPAI'],                         
#                                        'Imputation_comptable': '0',                                 
#                                        'Journal': recGP["Code_recette"],                             
#                                        'Heure_export_comptable': 0,                                 
#                                        'Heure_encaissement': 0}                                     
#                    listeNewDecEncGesProjet.append (NewDecaissement)
#                    del (NewDecaissement)
#                    del (recGP)            
        creationElementGp (listeNewDecEncGesProjet) 
    trace ('Recap  :')
    trace (f'--Nb enregistrement PIH parcouru = {globalNbParcouru}')
    trace (f'--Nb creation attendues :          {globalNbCreeTheorique}')
    trace (f'--Nb post pratiqué :               {globalNbPostGp}' )         
    if DoTrace :
        globalFicTrace.close ()
    
if __name__ == "__main__":
    doIt()
    print ('All Is right !')
