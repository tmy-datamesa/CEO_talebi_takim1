import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Navbar linkiyle uyumlu olduğundan emin olun (404 hatası almamak için)
dash.register_page(__name__, path="/hakkinda", name="Metodoloji")

# Stil Sabitleri
CARD_STYLE = {"borderRadius": "16px", "border": "none", "height": "100%"}
FLOW_CARD_STYLE = {"borderRadius": "12px", "border": "1px solid #0d6efd", "backgroundColor": "#f8f9ff"}

layout = dbc.Container([
    # 1. BÖLÜM: HOŞGELDİNİZ VE SUNUM AKIŞI (SENİN AÇILIŞIN)
    html.Div([
        html.H2("Olist Yönetim İçgörü Paneli", className="mt-4 fw-bold"),
        html.P("Operasyonel Verimlilikten Finansal Optimizasyona Veri Odaklı Yol Haritası", className="lead text-primary"),
    ]),

    # Sunum Yol Haritası (Burada hikayeyi anlatacaksın: Önce Müşteri, Sonra Finans, Sonra Kâr)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("1. ADIM", className="badge bg-primary mb-2"),
                    html.H5("Müşteri Deneyimi", className="fw-bold"),
                    html.P("Müşteri neden mutsuz? Memnuniyet sürücülerinin analizi.", className="small text-muted")
                ])
            ], style=FLOW_CARD_STYLE, className="text-center shadow-sm")
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("2. ADIM", className="badge bg-secondary mb-2"),
                    html.H5("Finansal Etki", className="fw-bold"),
                    html.P("Operasyonel hataların bugünkü kârlılığa net maliyeti.", className="small text-muted")
                ])
            ], style=CARD_STYLE, className="text-center shadow-sm border")
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("3. ADIM", className="badge bg-success mb-2"),
                    html.H5("Stratejik Aksiyon", className="fw-bold"),
                    html.P("Kârı maksimize edecek portföy optimizasyonu.", className="small text-muted")
                ])
            ], style=CARD_STYLE, className="text-center shadow-sm border")
        ], md=4),
    ], className="g-3 mb-5"),

    html.Hr(),

    # 2. BÖLÜM: METODOLOJİK TEMEL (SENİN BİLİMSEL KANITIN)
    html.H4("Matematiksel ve İstatistiksel Temel", className="mt-4 mb-3 fw-bold"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.B("Lojistik Regresyon (Logit)"), className="bg-white border-0 pt-3"),
                dbc.CardBody([
                    html.P("95.872 sipariş üzerinde wait_time ve delay etkileri ölçülmüştür."),
                    html.Div("Logit(P) = β₀ + β₁(wait_time) + β₂(delay) + ...", 
                             className="p-2 bg-light rounded small text-center font-monospace")
                ])
            ], style=CARD_STYLE, className="shadow-sm")
        ], md=6),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.B("Maliyet Fonksiyonu"), className="bg-white border-0 pt-3"),
                dbc.CardBody([
                    html.P("IT maliyetleri ölçek ekonomisi (karekök modeli) ile hesaplanmıştır."),
                    html.Div("$$Cost_{IT} = 3157.27 \\sqrt{n} + 978.23 \\sqrt{q}$$", 
                             className="p-2 bg-light rounded text-center")
                ])
            ], style=CARD_STYLE, className="shadow-sm")
        ], md=6),
    ], className="g-4 mb-4"),

    # Alt Bilgi: Teknik Künye
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([html.Small([html.B("Veri Hacmi: "), "95.872 Sipariş"])], md=4),
                dbc.Col([html.Small([html.B("Güven Aralığı: "), "%95 Konfidan"])], md=4),
                dbc.Col([html.Small([html.B("Araçlar: "), "Python, Dash, Statsmodels"])], md=4),
            ], className="text-muted")
        ])
    ], style=CARD_STYLE, className="shadow-sm bg-light")

], fluid=True, className="pb-5 px-4")