import streamlit as st
import math
import time

# ── EMBEDDED DATA FROM data.py ──
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
# ── END EMBEDDED DATA ──

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="Ventec KPI Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── COLORS ──
MPC = {
    'MPM1': '#1e3a8a', 'MPM2': '#059669', 'MPM3': '#7c3aed',
    'MPR4': '#dc2626', 'MPS1': '#ea580c', 'MPS2': '#0891b2',
    'MPS4': '#4f46e5', 'MPS5': '#b45309'
}
SC = {'v': '#15803d', 'o': '#b45309', 'r': '#b91c1c', 'g': '#475569'}
SD = {'v': '#22c55e', 'o': '#f59e0b', 'r': '#ef4444', 'g': '#94a3b8'}
SL = {'v': 'Atteint', 'o': 'Surveillance', 'r': 'Alerte', 'g': 'Non renseigné'}
SB_CSS = {'v': '#f0fdf4', 'o': '#fffbeb', 'r': '#fef2f2', 'g': '#f8fafc'}
ROLE_COLORS = {'admin': '#ef4444', 'manager': '#3b82f6', 'viewer': '#64748b'}
ROLE_LABELS = {'admin': 'Admin', 'manager': 'Manager', 'viewer': 'Lecteur'}

# ── UTILS ──
def get_status(k, v):
    if v is None:
        return 'g'
    if k['t'] == 'max':
        if v >= k['o']: return 'v'
        if v >= k['s']: return 'o'
        return 'r'
    else:
        if k['o'] == 0 and k['s'] == 0: return 'g'
        if v <= k['o']: return 'v'
        if v <= k['s']: return 'o'
        return 'r'

def fmt(v):
    if v is None: return '—'
    if abs(v) >= 10000: return f"{v:,.0f}".replace(',', ' ')
    if isinstance(v, int) or v == int(v): return str(int(v))
    if abs(v) < 1: return f"{v:.4f}"
    if abs(v) < 10: return f"{v:.2f}"
    return f"{v:.1f}"

def get_achievement_pct(k, val):
    if val is None or k['o'] == 0: return 0
    if k['t'] == 'max':
        return max(0, min(100, round((val / k['o']) * 100)))
    else:
        return max(0, min(100, round((k['o'] / val) * 100)))

# ── SESSION STATE INIT ──
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'kpi_data' not in st.session_state:
    st.session_state.kpi_data = gen_data()
if 'users' not in st.session_state:
    st.session_state.users = [u.copy() for u in USERS]
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = 5
if 'page' not in st.session_state:
    st.session_state.page = 'dash'

# ── CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stSidebarNav"] { display: none; }

/* Background */
.stApp { background: #f1f5f9; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #94a3b8 !important; }

/* Sidebar buttons */
.sidebar-btn {
    display: flex; align-items: center; gap: 10px;
    width: 100%; padding: 9px 12px; margin: 2px 0;
    border-radius: 8px; cursor: pointer; font-size: 13px;
    border: none; text-align: left; background: transparent;
    color: #94a3b8; font-weight: 500; transition: all .15s;
}
.sidebar-btn:hover { background: #1e293b; color: #fff; }
.sidebar-btn.active { background: #1d4ed8; color: #fff !important; }

/* Cards */
.kpi-card {
    background: #fff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,.06);
    transition: box-shadow .2s; margin-bottom: 4px;
}
.kpi-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,.1); }

.stat-card {
    background: #fff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 14px 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,.06);
}

/* Badges */
.badge {
    display: inline-block; border-radius: 20px;
    padding: 2px 10px; font-size: 11px; font-weight: 700;
}
.badge-mp {
    display: inline-block; border-radius: 4px;
    padding: 1px 5px; font-size: 9px; font-weight: 700;
}

/* Progress bar */
.progress-wrap {
    height: 5px; border-radius: 3px; background: #f1f5f9;
    overflow: hidden; margin: 6px 0;
}
.progress-bar { height: 100%; border-radius: 3px; transition: width .4s; }

/* Login */
.login-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    display: flex; align-items: center; justify-content: center;
}
.login-box {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 16px; padding: 32px;
}

/* Table */
.kpi-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.kpi-table th {
    padding: 10px 14px; text-align: left;
    font-size: 11px; font-weight: 700; color: #64748b;
    background: #f8fafc; border-bottom: 1px solid #e2e8f0;
}
.kpi-table td { padding: 10px 14px; border-bottom: 1px solid #f1f5f9; }

/* Streamlit overrides */
.stSelectbox > div > div { border-radius: 8px !important; border-color: #cbd5e1 !important; }
.stTextInput > div > div { border-radius: 8px !important; }
.stNumberInput > div > div { border-radius: 8px !important; }
div[data-testid="stHorizontalBlock"] { gap: 12px; }

/* Section label */
.section-label {
    font-size: 10px; text-transform: uppercase; letter-spacing: .8px;
    color: #475569; font-weight: 700; padding: 14px 0 4px;
}

/* Header bar */
.top-header {
    background: #fff; border-bottom: 1px solid #e2e8f0;
    padding: 12px 24px; display: flex; align-items: center;
    justify-content: space-between; margin-bottom: 24px;
    border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,.06);
}

/* Rapport section */
.rapport-header {
    padding: 12px 18px; display: flex; align-items: center; gap: 12px;
    border-bottom: 1px solid #e2e8f0; background: #f8fafc;
}

button[kind="secondary"] { border-radius: 8px !important; }
button[kind="primary"] { border-radius: 8px !important; }

/* Toast-like success */
div[data-testid="stAlert"] { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════
def render_login():
    st.markdown("""
    <div style="display:flex;justify-content:center;align-items:center;padding:40px 0 20px;">
        <svg width="240" height="74" viewBox="0 0 400 124">
            <rect x="0" y="0" width="400" height="124" rx="62" fill="#1e3a5f"/>
            <rect x="6" y="6" width="388" height="112" rx="56" fill="#0f2044"/>
            <text x="200" y="76" font-family="Arial" font-weight="800" font-size="40" fill="#fff" text-anchor="middle">VENTEC</text>
            <text x="200" y="98" font-family="Arial" font-weight="500" font-size="11" fill="#94a3b8" text-anchor="middle" letter-spacing="4">INDUSTRIES</text>
        </svg>
    </div>
    <p style="text-align:center;color:#64748b;font-size:13px;margin-bottom:30px;">Tableau de Bord KPI — 2026</p>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        with st.container():
            st.markdown("""
            <div style="background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.12);
                border-radius:16px;padding:28px 28px 8px;">
                <div style="font-size:18px;font-weight:700;color:#f1f5f9;margin-bottom:6px;">Connexion</div>
                <div style="font-size:13px;color:#64748b;margin-bottom:20px;">Accédez à votre espace de pilotage</div>
            </div>
            """, unsafe_allow_html=True)

            email = st.text_input("EMAIL", placeholder="email@ventec.ma", key="login_email")
            password = st.text_input("MOT DE PASSE", placeholder="••••••••", type="password", key="login_pwd")

            if 'login_error' in st.session_state and st.session_state.login_error:
                st.error(st.session_state.login_error)

            if st.button("Se connecter", use_container_width=True, type="primary"):
                user = next((u for u in st.session_state.users
                             if u['e'] == email.strip() and u['p'] == password and u['a']), None)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user
                    st.session_state.login_error = ''
                    st.rerun()
                else:
                    st.session_state.login_error = '❌ Email ou mot de passe incorrect'
                    st.rerun()

            st.markdown("---")
            st.markdown("<div style='font-size:11px;color:#475569;font-weight:600;margin-bottom:8px;'>Comptes de démo</div>", unsafe_allow_html=True)
            for u in USERS:
                role_color = '#fca5a5' if u['ro'] == 'admin' else '#93c5fd' if u['ro'] == 'manager' else '#94a3b8'
                role_bg = 'rgba(239,68,68,.2)' if u['ro'] == 'admin' else 'rgba(59,130,246,.2)' if u['ro'] == 'manager' else 'rgba(148,163,184,.15)'
                if st.button(f"👤 {u['n']} — {u['e']}", key=f"demo_{u['id']}", use_container_width=True):
                    st.session_state.logged_in = True
                    st.session_state.current_user = u.copy()
                    st.session_state.login_error = ''
                    st.rerun()

# ══════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════
def render_sidebar():
    cu = st.session_state.current_user
    is_admin = cu['ro'] == 'admin'

    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:8px 0 12px;border-bottom:1px solid #1e293b;">
            <svg width="160" height="50" viewBox="0 0 400 124">
                <rect x="0" y="0" width="400" height="124" rx="62" fill="#1e3a5f"/>
                <rect x="6" y="6" width="388" height="112" rx="56" fill="#0f2044"/>
                <text x="200" y="76" font-family="Arial" font-weight="800" font-size="40" fill="#fff" text-anchor="middle">VENTEC</text>
                <text x="200" y="98" font-family="Arial" font-weight="500" font-size="11" fill="#94a3b8" text-anchor="middle" letter-spacing="4">INDUSTRIES</text>
            </svg>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-label" style="color:#475569;padding-left:4px;">Navigation</div>', unsafe_allow_html=True)

        nav_items = [
            ('dash', '▦', 'Vue globale'),
            ('saisie', '✏', 'Saisie'),
            ('rapport', '📊', 'Rapport'),
        ]
        if is_admin:
            nav_items.append(('users', '👥', 'Utilisateurs'))

        for page_id, icon, label in nav_items:
            is_active = st.session_state.page == page_id
            btn_style = "background:#1d4ed8;color:#fff;" if is_active else ""
            if st.button(f"{icon}  {label}", key=f"nav_{page_id}",
                        use_container_width=True,
                        type="primary" if is_active else "secondary"):
                st.session_state.page = page_id
                st.rerun()

        st.markdown('<div class="section-label" style="color:#475569;padding-left:4px;">Macro-Processus</div>', unsafe_allow_html=True)

        for mp_id in MP_LIST:
            mp = MACRO_PROCESSES[mp_id]
            color = MPC[mp_id]
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:5px 8px;color:#64748b;font-size:11px;">
                <span style="width:8px;height:8px;border-radius:50%;background:{color};display:inline-block;flex-shrink:0;"></span>
                <span style="flex:1;">{mp['c']}</span>
                <span style="font-size:9px;color:#475569;">{len(mp['k'])} KPIs</span>
            </div>
            """, unsafe_allow_html=True)

        # User info + logout
        role_color = ROLE_COLORS.get(cu['ro'], '#64748b')
        st.markdown(f"""
        <div style="margin-top:auto;padding:14px 4px;border-top:1px solid #1e293b;font-size:11px;color:#475569;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <div style="width:28px;height:28px;border-radius:50%;background:{role_color};
                    display:flex;align-items:center;justify-content:center;
                    font-size:13px;font-weight:700;color:#fff;flex-shrink:0;">{cu['n'][0]}</div>
                <div>
                    <div style="font-size:12px;font-weight:600;color:#e2e8f0;">{cu['n']}</div>
                    <div style="font-size:10px;color:#94a3b8;">{ROLE_LABELS.get(cu['ro'],'')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Déconnexion", key="logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.page = 'dash'
            st.rerun()

# ══════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════
def render_dashboard():
    data = st.session_state.kpi_data
    mo = st.session_state.selected_month

    # Header row
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<h2 style='margin:0;font-size:20px;font-weight:700;'>Vue globale</h2><p style='color:#64748b;font-size:12px;margin:0;'>44 KPIs · 8 Macro-Processus</p>", unsafe_allow_html=True)
    with col2:
        mo = st.selectbox("Période", options=list(range(1, 7)),
                          format_func=lambda x: f"{MONTHS_LONG[x]} 2026",
                          index=mo - 1, key="dash_month")
        st.session_state.selected_month = mo

    # Stats
    v_count = o_count = r_count = 0
    for k in KPIS:
        s = get_status(k, data.get(k['i'], {}).get(mo))
        if s == 'v': v_count += 1
        elif s == 'o': o_count += 1
        elif s == 'r': r_count += 1
    tx = round((v_count / len(KPIS)) * 100)
    tx_color = '#15803d' if tx >= 80 else '#b45309' if tx >= 60 else '#b91c1c'

    cols = st.columns(5)
    stats = [
        ('Total KPIs', len(KPIS), '#1d4ed8', 'Indicateurs'),
        ('✓ Atteints', v_count, '#15803d', 'Objectif'),
        ('⚠ Surveillance', o_count, '#b45309', 'Entre obj. et seuil'),
        ('✗ Alertes', r_count, '#b91c1c', 'Sous seuil'),
        ('Taux', f"{tx}%", tx_color, 'Global'),
    ]
    for col, (label, val, color, sub) in zip(cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:11px;color:#64748b;font-weight:600;margin-bottom:6px;">{label}</div>
                <div style="font-size:28px;font-weight:700;color:{color};">{val}</div>
                <div style="font-size:11px;color:#94a3b8;margin-top:4px;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    # Progress bar
    vp = v_count / len(KPIS) * 100
    op = o_count / len(KPIS) * 100
    rp = r_count / len(KPIS) * 100
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:12px 16px;margin:16px 0 8px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
            <span style="font-size:12px;font-weight:600;">Répartition</span>
            <div style="display:flex;gap:16px;font-size:11px;color:#94a3b8;">
                <span><span style="width:8px;height:8px;border-radius:50%;background:#22c55e;display:inline-block;margin-right:4px;"></span>Atteints</span>
                <span><span style="width:8px;height:8px;border-radius:50%;background:#f59e0b;display:inline-block;margin-right:4px;"></span>Surveillance</span>
                <span><span style="width:8px;height:8px;border-radius:50%;background:#ef4444;display:inline-block;margin-right:4px;"></span>Alerte</span>
            </div>
        </div>
        <div style="height:10px;border-radius:5px;background:#f1f5f9;overflow:hidden;display:flex;">
            <div style="height:100%;width:{vp:.1f}%;background:#22c55e;"></div>
            <div style="height:100%;width:{op:.1f}%;background:#f59e0b;"></div>
            <div style="height:100%;width:{rp:.1f}%;background:#ef4444;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filters
    fc1, fc2, fc3, fc4 = st.columns([2, 2, 1.5, 1])
    with fc1:
        search = st.text_input("🔍", placeholder="Rechercher...", label_visibility="collapsed", key="dash_search")
    with fc2:
        mp_filter = st.selectbox("MP", ["Tous"] + MP_LIST,
                                  format_func=lambda x: "Tous MP" if x == "Tous" else f"{x} — {MACRO_PROCESSES[x]['n']}",
                                  label_visibility="collapsed", key="dash_mp")
    with fc3:
        status_filter = st.selectbox("Statut", ["Tous", "v", "o", "r"],
                                      format_func=lambda x: {"Tous": "Tous statuts", "v": "✓ Atteints", "o": "⚠ Surveillance", "r": "✗ Alertes"}[x],
                                      label_visibility="collapsed", key="dash_status")
    with fc4:
        view_mode = st.selectbox("Vue", ["grid", "group"],
                                  format_func=lambda x: "Grille" if x == "grid" else "Par MP",
                                  label_visibility="collapsed", key="dash_view")

    # Filter KPIs
    filtered = [k for k in KPIS
                if (not search or search.lower() in k['n'].lower() or search.lower() in k['c'].lower())
                and (mp_filter == "Tous" or k['m'] == mp_filter)
                and (status_filter == "Tous" or get_status(k, data.get(k['i'], {}).get(mo)) == status_filter)]

    if not filtered:
        st.info("Aucun KPI trouvé")
        return

    def render_kpi_card(k):
        val = data.get(k['i'], {}).get(mo)
        s = get_status(k, val)
        pct = get_achievement_pct(k, val)
        prev = data.get(k['i'], {}).get(mo - 1)
        trend = None
        if prev is not None and val is not None:
            trend = '↑' if val > prev else '↓' if val < prev else '→'
        trend_color = '#94a3b8'
        if trend == '↑':
            trend_color = '#15803d' if k['t'] == 'max' else '#b91c1c'
        elif trend == '↓':
            trend_color = '#15803d' if k['t'] == 'min' else '#b91c1c'

        border_colors = {'v': '#22c55e', 'o': '#f59e0b', 'r': '#ef4444', 'g': '#e2e8f0'}
        badge_bg = {'v': '#f0fdf4', 'o': '#fffbeb', 'r': '#fef2f2', 'g': '#f8fafc'}
        badge_border = {'v': '#bbf7d0', 'o': '#fde68a', 'r': '#fecaca', 'g': '#e2e8f0'}
        mp_bg = {'MPM1':'#eff6ff','MPM2':'#ecfdf5','MPM3':'#f5f3ff','MPR4':'#fef2f2',
                 'MPS1':'#fff7ed','MPS2':'#ecfeff','MPS4':'#eef2ff','MPS5':'#fffbeb'}
        mp_bd = {'MPM1':'#bfdbfe','MPM2':'#a7f3d0','MPM3':'#ddd6fe','MPR4':'#fecaca',
                 'MPS1':'#fed7aa','MPS2':'#a5f3fc','MPS4':'#c7d2fe','MPS5':'#fde68a'}

        trend_html = f'<span style="font-size:13px;font-weight:700;color:{trend_color};margin-left:auto;">{trend}</span>' if trend else ''
        val_display = fmt(val)
        bc = border_colors[s]
        mp_id = k['m']

        st.markdown(f"""
        <div class="kpi-card" style="border-left:4px solid {bc};">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                <span style="font-size:10px;color:#94a3b8;font-weight:700;">{k['c']}</span>
                <span class="badge-mp" style="background:{mp_bg[mp_id]};color:{MPC[mp_id]};border:1px solid {mp_bd[mp_id]};">{mp_id}</span>
            </div>
            <div style="font-size:13px;font-weight:600;color:#1e293b;line-height:1.3;margin-bottom:10px;min-height:34px;">{k['n']}</div>
            <div style="display:flex;align-items:baseline;gap:6px;margin-bottom:4px;">
                <span style="font-size:26px;font-weight:700;color:{SC[s]};">{val_display}</span>
                <span style="font-size:12px;color:#64748b;">{k['u']}</span>
                {trend_html}
            </div>
            <div style="display:flex;justify-content:space-between;font-size:11px;color:#94a3b8;margin-bottom:6px;">
                <span>Obj. {k['o']}</span><span>Seuil {k['s']}</span>
            </div>
            <div class="progress-wrap">
                <div class="progress-bar" style="width:{pct}%;background:{SD[s]};"></div>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px;">
                <span class="badge" style="background:{badge_bg[s]};color:{SC[s]};border:1px solid {badge_border[s]};">{SL[s]}</span>
                <span style="font-size:10px;color:#94a3b8;">{k['r']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if view_mode == "grid":
        cols_per_row = 3
        rows = [filtered[i:i+cols_per_row] for i in range(0, len(filtered), cols_per_row)]
        for row in rows:
            cols = st.columns(cols_per_row)
            for col, k in zip(cols, row):
                with col:
                    render_kpi_card(k)
    else:
        for mp_id in MP_LIST:
            kmp = [k for k in filtered if k['m'] == mp_id]
            if not kmp: continue
            mi = MACRO_PROCESSES[mp_id]
            av = sum(1 for k in kmp if get_status(k, data.get(k['i'], {}).get(mo)) == 'v')
            ao = sum(1 for k in kmp if get_status(k, data.get(k['i'], {}).get(mo)) == 'o')
            ar = sum(1 for k in kmp if get_status(k, data.get(k['i'], {}).get(mo)) == 'r')
            color = MPC[mp_id]
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;margin:16px 0 8px;
                padding:10px 14px;background:#fff;border:1px solid #e2e8f0;border-radius:10px;">
                <span style="width:12px;height:12px;border-radius:50%;background:{color};display:inline-block;"></span>
                <span style="font-size:13px;font-weight:700;">{mi['c']} — {mi['n']}</span>
                <span style="font-size:10px;color:#94a3b8;">{mi['r']}</span>
                <span style="margin-left:auto;font-size:11px;color:#15803d;font-weight:600;">✓ {av}</span>
                <span style="font-size:11px;color:#b45309;font-weight:600;margin-left:8px;">⚠ {ao}</span>
                <span style="font-size:11px;color:#b91c1c;font-weight:600;margin-left:8px;">✗ {ar}</span>
            </div>
            """, unsafe_allow_html=True)
            cols_per_row = 3
            rows = [kmp[i:i+cols_per_row] for i in range(0, len(kmp), cols_per_row)]
            for row in rows:
                cols = st.columns(cols_per_row)
                for col, k in zip(cols, row):
                    with col:
                        render_kpi_card(k)

# ══════════════════════════════════════════════════
# SAISIE
# ══════════════════════════════════════════════════
def render_saisie():
    cu = st.session_state.current_user
    can_edit = cu['ro'] in ('admin', 'manager')

    if not can_edit:
        st.markdown("<div style='text-align:center;padding:60px;color:#94a3b8;'>Accès réservé</div>", unsafe_allow_html=True)
        return

    data = st.session_state.kpi_data

    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    with col1:
        mo = st.selectbox("Mois", list(range(1, 7)),
                          format_func=lambda x: f"{MONTHS_LONG[x]} 2026",
                          index=5, key="saisie_month")
    with col2:
        mp_filter = st.selectbox("MP", [""] + MP_LIST,
                                  format_func=lambda x: "Tous MP" if x == "" else x,
                                  key="saisie_mp")

    kpis_to_show = [k for k in KPIS if not mp_filter or k['m'] == mp_filter]

    if 'saisie_vals' not in st.session_state:
        st.session_state.saisie_vals = {}

    st.markdown("---")

    # Table header
    st.markdown("""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;">
    <table class="kpi-table" style="width:100%;">
        <thead><tr style="background:#f8fafc;border-bottom:1px solid #e2e8f0;">
            <th>Code</th><th>Indicateur</th><th>Unité</th>
            <th style="text-align:right;">Obj</th><th style="text-align:right;">Seuil</th>
            <th style="text-align:right;">Précédent</th><th>Statut</th>
        </tr></thead>
    </table>
    </div>
    """, unsafe_allow_html=True)

    save_vals = {}
    for k in kpis_to_show:
        cur = data.get(k['i'], {}).get(mo)
        prev = data.get(k['i'], {}).get(mo - 1)
        s = get_status(k, cur)

        mp_bg = {'MPM1':'#eff6ff','MPM2':'#ecfdf5','MPM3':'#f5f3ff','MPR4':'#fef2f2',
                 'MPS1':'#fff7ed','MPS2':'#ecfeff','MPS4':'#eef2ff','MPS5':'#fffbeb'}
        mp_bd = {'MPM1':'#bfdbfe','MPM2':'#a7f3d0','MPM3':'#ddd6fe','MPR4':'#fecaca',
                 'MPS1':'#fed7aa','MPS2':'#a5f3fc','MPS4':'#c7d2fe','MPS5':'#fde68a'}

        c1, c2, c3, c4, c5, c6, c7 = st.columns([1.2, 3, 1, 0.8, 0.8, 1, 1.5])
        with c1:
            st.markdown(f"""
            <div style="padding:6px 0;">
                <div style="font-size:10px;color:#94a3b8;font-weight:700;">{k['c']}</div>
                <span style="font-size:9px;background:{mp_bg[k['m']]};color:{MPC[k['m']]};
                    border:1px solid {mp_bd[k['m']]};border-radius:3px;padding:1px 4px;font-weight:700;">{k['m']}</span>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div style='font-weight:500;font-size:13px;padding:8px 0;'>{k['n']}</div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div style='font-size:11px;color:#64748b;padding:8px 0;'>{k['u']}</div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div style='font-weight:600;padding:8px 0;font-size:13px;'>{k['o']}</div>", unsafe_allow_html=True)
        with c5:
            st.markdown(f"<div style='color:#94a3b8;padding:8px 0;font-size:13px;'>{k['s']}</div>", unsafe_allow_html=True)
        with c6:
            st.markdown(f"<div style='color:#94a3b8;padding:8px 0;font-size:13px;'>{fmt(prev) if prev is not None else '—'}</div>", unsafe_allow_html=True)
        with c7:
            new_val = st.number_input("val", value=float(cur) if cur is not None else None,
                                      placeholder=fmt(cur) if cur is not None else "—",
                                      key=f"saisie_{k['i']}_{mo}",
                                      label_visibility="collapsed", step=0.01)
            if new_val is not None:
                save_vals[k['i']] = new_val

        st.divider()

    col_r, col_s = st.columns([6, 1])
    with col_r:
        if st.button("✕ Reset", key="saisie_reset"):
            st.rerun()
    with col_s:
        if st.button("✓ Enregistrer", type="primary", key="saisie_save"):
            count = 0
            nd = {kk: dict(vv) for kk, vv in data.items()}
            for kid, val in save_vals.items():
                if val is not None:
                    if kid not in nd: nd[kid] = {}
                    nd[kid][mo] = val
                    count += 1
            if count > 0:
                st.session_state.kpi_data = nd
                st.success(f"✓ {count} valeur(s) enregistrée(s)")
            else:
                st.warning("Aucune valeur à enregistrer")

# ══════════════════════════════════════════════════
# RAPPORT
# ══════════════════════════════════════════════════
def render_rapport():
    data = st.session_state.kpi_data

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h2 style='margin:0;font-size:16px;font-weight:700;'>Rapport par Macro-Processus</h2>", unsafe_allow_html=True)
    with col2:
        mo = st.selectbox("Mois", list(range(1, 7)),
                          format_func=lambda x: f"{MONTHS_LONG[x]} 2026",
                          index=4, key="rapport_month")

    st.markdown(f"<p style='color:#64748b;font-size:12px;margin-bottom:16px;'>{MONTHS_LONG[mo]} 2026</p>", unsafe_allow_html=True)

    for mp_id in MP_LIST:
        kpis = [k for k in KPIS if k['m'] == mp_id]
        v = sum(1 for k in kpis if get_status(k, data.get(k['i'], {}).get(mo)) == 'v')
        o = sum(1 for k in kpis if get_status(k, data.get(k['i'], {}).get(mo)) == 'o')
        r = sum(1 for k in kpis if get_status(k, data.get(k['i'], {}).get(mo)) == 'r')
        tx = round((v / len(kpis)) * 100)
        tc = '#15803d' if tx >= 80 else '#b45309' if tx >= 60 else '#b91c1c'
        mi = MACRO_PROCESSES[mp_id]
        color = MPC[mp_id]

        rows_html = ""
        for k in kpis:
            val = data.get(k['i'], {}).get(mo)
            s = get_status(k, val)
            ta = get_achievement_pct(k, val)
            ta_str = f"{ta}%" if val is not None else "—"
            rows_html += f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                padding:8px 0;border-bottom:1px solid #f1f5f9;">
                <div style="flex:1;">
                    <div style="font-weight:500;font-size:12px;">{k['n']}</div>
                    <div style="font-size:10px;color:#94a3b8;">{k['c']}</div>
                </div>
                <div style="text-align:right;margin-right:16px;">
                    <div style="font-weight:700;color:{SC[s]};">{fmt(val)} {k['u']}</div>
                    <div style="font-size:10px;color:#94a3b8;">Obj: {k['o']}</div>
                </div>
                <div style="width:80px;text-align:right;">
                    <div style="font-size:11px;font-weight:600;color:{SC[s]};">{ta_str}</div>
                </div>
            </div>"""

        st.markdown(f"""
        <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;
            margin-bottom:16px;overflow:hidden;">
            <div style="padding:12px 18px;display:flex;align-items:center;gap:12px;
                border-bottom:1px solid #e2e8f0;background:#f8fafc;">
                <span style="width:14px;height:14px;border-radius:50%;background:{color};
                    display:inline-block;flex-shrink:0;"></span>
                <div style="flex:1;">
                    <span style="font-size:13px;font-weight:700;">{mi['c']} — {mi['n']}</span>
                    <span style="font-size:10px;color:#94a3b8;margin-left:8px;">{mi['r']}</span>
                </div>
                <span style="background:#f0fdf4;color:#15803d;border:1px solid #bbf7d0;
                    border-radius:20px;padding:2px 8px;font-size:10px;font-weight:700;">✓ {v}</span>
                <span style="background:#fffbeb;color:#b45309;border:1px solid #fde68a;
                    border-radius:20px;padding:2px 8px;font-size:10px;font-weight:700;">⚠ {o}</span>
                <span style="background:#fef2f2;color:#b91c1c;border:1px solid #fecaca;
                    border-radius:20px;padding:2px 8px;font-size:10px;font-weight:700;">✗ {r}</span>
                <span style="font-size:18px;font-weight:800;color:{tc};">{tx}%</span>
            </div>
            <div style="padding:10px 18px;">{rows_html}</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# USERS
# ══════════════════════════════════════════════════
def render_users():
    cu = st.session_state.current_user
    users = st.session_state.users

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<h2 style='margin:0;font-size:16px;font-weight:700;'>Utilisateurs</h2><p style='font-size:12px;color:#64748b;margin:0;'>{len(users)} compte(s)</p>", unsafe_allow_html=True)
    with col2:
        show_form = st.button("+ Nouveau", type="primary")

    if show_form or st.session_state.get('show_user_form'):
        st.session_state.show_user_form = True
        with st.expander("Créer / Modifier utilisateur", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                new_name = st.text_input("Nom", key="uf_name")
                new_email = st.text_input("Email", key="uf_email")
            with c2:
                new_pwd = st.text_input("Mot de passe", type="password", key="uf_pwd")
                new_role = st.selectbox("Rôle", ["viewer", "manager", "admin"],
                                        format_func=lambda x: {"viewer": "Lecteur", "manager": "Manager", "admin": "Admin"}[x],
                                        key="uf_role")
            new_active = st.checkbox("Actif", value=True, key="uf_active")
            if st.button("✓ Enregistrer", type="primary", key="uf_save"):
                if not new_name or not new_email or not new_pwd:
                    st.error("Champs requis")
                else:
                    st.session_state.users.append({
                        'id': int(time.time()), 'n': new_name, 'e': new_email,
                        'p': new_pwd, 'ro': new_role, 'a': new_active
                    })
                    st.session_state.show_user_form = False
                    st.success("Utilisateur créé")
                    st.rerun()

    rc = {'admin': ('#fef2f2', '#b91c1c'), 'manager': ('#eff6ff', '#1d4ed8'), 'viewer': ('#f8fafc', '#475569')}
    rl = {'admin': 'Admin', 'manager': 'Manager', 'viewer': 'Lecteur'}

    table_rows = ""
    for u in users:
        is_me = u['id'] == cu['id']
        rbg, rc_c = rc[u['ro']]
        active_bg = '#f0fdf4' if u['a'] else '#f8fafc'
        active_c = '#15803d' if u['a'] else '#94a3b8'
        me_badge = '<span style="font-size:10px;color:#94a3b8;"> (vous)</span>' if is_me else ''
        delete_btn = '' if is_me else f'<span style="color:#b91c1c;font-size:11px;cursor:pointer;">Suppr</span>'
        table_rows += f"""
        <tr style="border-bottom:1px solid #f1f5f9;">
            <td style="padding:12px 16px;font-weight:600;">{u['n']}{me_badge}</td>
            <td style="padding:12px 16px;color:#475569;font-size:12px;">{u['e']}</td>
            <td style="padding:12px 16px;">
                <span style="background:{rbg};color:{rc_c};border-radius:20px;padding:2px 10px;font-size:11px;font-weight:700;">{rl[u['ro']]}</span>
            </td>
            <td style="padding:12px 16px;">
                <span style="background:{active_bg};color:{active_c};border-radius:20px;padding:2px 10px;font-size:11px;font-weight:700;">{'Actif' if u['a'] else 'Inactif'}</span>
            </td>
        </tr>"""

    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;margin-top:16px;">
        <table style="width:100%;border-collapse:collapse;font-size:13px;">
            <thead><tr style="background:#f8fafc;border-bottom:1px solid #e2e8f0;">
                <th style="padding:10px 16px;text-align:left;font-size:11px;font-weight:700;color:#64748b;">Nom</th>
                <th style="padding:10px 16px;text-align:left;font-size:11px;font-weight:700;color:#64748b;">Email</th>
                <th style="padding:10px 16px;text-align:left;font-size:11px;font-weight:700;color:#64748b;">Rôle</th>
                <th style="padding:10px 16px;text-align:left;font-size:11px;font-weight:700;color:#64748b;">Statut</th>
            </tr></thead>
            <tbody>{table_rows}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        render_login()
        return

    render_sidebar()

    page = st.session_state.page
    page_titles = {'dash': 'Vue globale', 'saisie': 'Saisie', 'rapport': 'Rapport', 'users': 'Utilisateurs'}

    if page == 'dash':
        render_dashboard()
    elif page == 'saisie':
        render_saisie()
    elif page == 'rapport':
        render_rapport()
    elif page == 'users':
        if st.session_state.current_user['ro'] == 'admin':
            render_users()
        else:
            st.error("Accès réservé aux administrateurs")

if __name__ == "__main__":
    main()
