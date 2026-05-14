import math

MONTHS_SHORT = ['', 'Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
MONTHS_LONG  = ['', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

MACRO_PROCESSES = {
    'MPM1': {'c': 'MPM1', 'n': 'Management SSE et Performance financière', 'r': 'Directeur Générale',       'k': [1,2,4,5,26]},
    'MPM2': {'c': 'MPM2', 'n': 'Management RH et Environnement',           'r': 'Secrétariat Générale',     'k': [11,12,13,14]},
    'MPM3': {'c': 'MPM3', 'n': 'Management Recrutement et RH',             'r': 'Chef de Service Capital Humain', 'k': [21,22,23,24,25]},
    'MPR4': {'c': 'MPR4', 'n': 'Réalisation Production',                   'r': 'Directeur Atelier',        'k': [6,19,20,36,37,38,39,40,41]},
    'MPS1': {'c': 'MPS1', 'n': 'Support Achats',                           'r': 'Chef de Service Achat',    'k': [27,42,43,44]},
    'MPS2': {'c': 'MPS2', 'n': 'Support Logistique et Stock',              'r': 'R Logistique',             'k': [3,28,29,30,31]},
    'MPS4': {'c': 'MPS4', 'n': 'Support Ressources',                       'r': 'Chef de Service SI',       'k': [32,33,34,35]},
    'MPS5': {'c': 'MPS5', 'n': 'Support Maintenance et Énergie',           'r': 'Chef de Service MG',       'k': [7,8,9,10,15,16,17,18]},
}
MP_LIST = ['MPM1', 'MPM2', 'MPM3', 'MPR4', 'MPS1', 'MPS2', 'MPS4', 'MPS5']

KPIS = [
    {'i':1,  'c':'KPI001','n':'Taux de satisfaction client',   'u':'%',      'o':95,    's':90,    't':'max','m':'MPM1','r':'DG'},
    {'i':2,  'c':'KPI002','n':'Notoriété digitale',            'u':'abonnés','o':180000,'s':180000,'t':'max','m':'MPM1','r':'DG'},
    {'i':3,  'c':'KPI003','n':'Taux de réclamations',          'u':'%',      'o':0,     's':1,     't':'min','m':'MPS2','r':'R.QSE'},
    {'i':4,  'c':'KPI004','n':'CA cumulé',                     'u':'M DH',   'o':105,   's':105,   't':'max','m':'MPM1','r':'DG'},
    {'i':5,  'c':'KPI005','n':'Rentabilité',                   'u':'%',      'o':8,     's':5,     't':'max','m':'MPM1','r':'DG'},
    {'i':6,  'c':'KPI006','n':'Production / Heure',            'u':'DH HT',  'o':160,   's':150,   't':'max','m':'MPR4','r':'Dir.Atelier'},
    {'i':7,  'c':'KPI007','n':'Conformité SSE',                'u':'%',      'o':100,   's':98,    't':'max','m':'MPS5','r':'DG'},
    {'i':8,  'c':'KPI008','n':'Fréquence accidents',           'u':'taux',   'o':10,    's':12,    't':'min','m':'MPS5','r':'R.HSE'},
    {'i':9,  'c':'KPI009','n':'Gravité accidents',             'u':'taux',   'o':0.3,   's':0.35,  't':'min','m':'MPS5','r':'R.HSE'},
    {'i':10, 'c':'KPI010','n':'Réalisation SSE',               'u':'%',      'o':100,   's':95,    't':'max','m':'MPS5','r':'R.QSE'},
    {'i':11, 'c':'KPI011','n':'Recyclage déchets',             'u':'%',      'o':65,    's':60,    't':'max','m':'MPM2','r':'R.QSE'},
    {'i':12, 'c':'KPI012','n':'Consommation gasoil',           'u':'L/Km',   'o':0.06,  's':0.065, 't':'min','m':'MPM2','r':'Resp.Log.'},
    {'i':13, 'c':'KPI013','n':'Réduction carburant',           'u':'indice', 'o':-0.05,'s':-0.05, 't':'min','m':'MPM2','r':'Resp.Log.'},
    {'i':14, 'c':'KPI014','n':'Réduction électricité',         'u':'%',      'o':-5,    's':0,     't':'min','m':'MPM2','r':'Chef MG'},
    {'i':15, 'c':'KPI015','n':'Audits internes',               'u':'%',      'o':100,   's':95,    't':'max','m':'MPS5','r':'R.QSE'},
    {'i':16, 'c':'KPI016','n':'Levées NC',                     'u':'%',      'o':100,   's':100,   't':'max','m':'MPS5','r':'Chef MG'},
    {'i':17, 'c':'KPI017','n':'Clôture demandes',              'u':'%',      'o':100,   's':90,    't':'max','m':'MPS5','r':'Chef MG'},
    {'i':18, 'c':'KPI018','n':'Maintenance préventive',        'u':'%',      'o':100,   's':90,    't':'max','m':'MPS5','r':'Chef MG'},
    {'i':19, 'c':'KPI019','n':'Chute de la tôle',              'u':'%',      'o':5,     's':6.5,   't':'min','m':'MPR4','r':'Dir.Atelier'},
    {'i':20, 'c':'KPI020','n':'Non-conformité prod',           'u':'%',      'o':0,     's':0.2,   't':'min','m':'MPR4','r':'Dir.Atelier'},
    {'i':21, 'c':'KPI021','n':'Satisfaction personnel',        'u':'%',      'o':80,    's':70,    't':'max','m':'MPM3','r':'DG'},
    {'i':22, 'c':'KPI022','n':'Délai recrutement',             'u':'jours',  'o':30,    's':30,    't':'min','m':'MPM3','r':'Chef DRH'},
    {'i':23, 'c':'KPI023','n':'Taux démission',                'u':'%',      'o':5,     's':8,     't':'min','m':'MPM3','r':'Chef DRH'},
    {'i':24, 'c':'KPI024','n':'Efficacité recrutement',        'u':'jours',  'o':30,    's':35,    't':'min','m':'MPM3','r':'Chef DRH'},
    {'i':25, 'c':'KPI025','n':'Plan formation',                'u':'%',      'o':90,    's':85,    't':'max','m':'MPM3','r':'Chef DRH'},
    {'i':26, 'c':'KPI026','n':'Objectifs QSE',                 'u':'%',      'o':90,    's':80,    't':'max','m':'MPM1','r':'DG'},
    {'i':27, 'c':'KPI027','n':"Frais d'approche",              'u':'%',      'o':9.5,   's':10.5,  't':'min','m':'MPS1','r':'Dir.Achat'},
    {'i':28, 'c':'KPI028','n':'Écart inventaire',              'u':'%',      'o':0.1,   's':0.15,  't':'min','m':'MPS2','r':'Resp.Log.'},
    {'i':29, 'c':'KPI029','n':'Rupture stock',                 'u':'%',      'o':2,     's':4,     't':'min','m':'MPS2','r':'Resp.Log.'},
    {'i':30, 'c':'KPI030','n':'Courses dans délais',           'u':'%',      'o':98,    's':95,    't':'max','m':'MPS2','r':'Resp.Log.'},
    {'i':31, 'c':'KPI031','n':'Délai outillage',               'u':'jours',  'o':3,     's':5,     't':'min','m':'MPS2','r':'Resp.Log.'},
    {'i':32, 'c':'KPI032','n':'Dispo infrastructures',         'u':'%',      'o':100,   's':95,    't':'max','m':'MPS4','r':'Chef SI'},
    {'i':33, 'c':'KPI033','n':'Dispo ressources SI',           'u':'%',      'o':98,    's':95,    't':'max','m':'MPS4','r':'Chef SI'},
    {'i':34, 'c':'KPI034','n':'Sécurité informatique',         'u':'%',      'o':100,   's':100,   't':'max','m':'MPS4','r':'Chef SI'},
    {'i':35, 'c':'KPI035','n':'Satisfaction SI',               'u':'%',      'o':85,    's':80,    't':'max','m':'MPS4','r':'Chef SI'},
    {'i':36, 'c':'KPI036','n':'Délai fabrication',             'u':'%',      'o':8.5,   's':9,     't':'min','m':'MPR4','r':'Dir.Atelier'},
    {'i':37, 'c':'KPI037','n':'Productivité',                  'u':'indice', 'o':1,     's':0.9,   't':'max','m':'MPR4','r':'Dir.Atelier'},
    {'i':38, 'c':'KPI038','n':'Production mensuelle',          'u':'M DH',   'o':13.5,  's':12,    't':'max','m':'MPR4','r':'Dir.Atelier'},
    {'i':39, 'c':'KPI039','n':'Disponibilité machine',         'u':'%',      'o':90,    's':80,    't':'max','m':'MPR4','r':'Dir.Atelier'},
    {'i':40, 'c':'KPI040','n':'Formation Fabrication',         'u':'%',      'o':90,    's':85,    't':'max','m':'MPR4','r':'Dir.Atelier'},
    {'i':41, 'c':'KPI041','n':'Gaines spiralées',              'u':'unités', 'o':0,     's':0,     't':'max','m':'MPR4','r':'Dir.Atelier'},
    {'i':42, 'c':'KPI042','n':'Commandes VM >48h',             'u':'%',      'o':1,     's':1.3,   't':'min','m':'MPS1','r':'Dir.Achat'},
    {'i':43, 'c':'KPI043','n':'Délai Carrier',                 'u':'sem.',   'o':1,     's':2,     't':'min','m':'MPS1','r':'Dir.Achat'},
    {'i':44, 'c':'KPI044','n':'Délai autres fourn.',           'u':'sem.',   'o':1,     's':2,     't':'min','m':'MPS1','r':'Dir.Achat'},
]

USERS = [
    {'id': 1, 'n': 'Administrateur', 'e': 'admin@ventec.ma',   'p': 'admin123',   'ro': 'admin',   'a': True},
    {'id': 2, 'n': 'Manager QSE',    'e': 'manager@ventec.ma', 'p': 'manager123', 'ro': 'manager', 'a': True},
    {'id': 3, 'n': 'Lecteur',        'e': 'viewer@ventec.ma',  'p': 'viewer123',  'ro': 'viewer',  'a': True},
]

def gen_data():
    d = {}
    s = 42
    def rng():
        nonlocal s
        s = math.sin(s) * 1e4
        return s - math.floor(s)

    for k in KPIS:
        d[k['i']] = {}
        for m in range(1, 6):
            r = rng()
            if k['t'] == 'max':
                b = k['o'] * (0.85 + r * 0.3)
            else:
                if k['o'] == 0:
                    b = r * (k['s'] or 1) * 1.2
                else:
                    b = k['o'] * (0.8 + r * 0.5)
            # round like the original
            if k['o'] >= 100:
                b = round(b, 0)
            elif k['o'] >= 10:
                b = round(b, 1)
            elif k['o'] >= 1:
                b = round(b, 2)
            else:
                b = round(b, 4)
            d[k['i']][m] = float(b)
    return d
