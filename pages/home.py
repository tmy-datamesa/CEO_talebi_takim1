# pages/home.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from olist.seller_updated import Seller

dash.register_page(__name__, path="/", name="Finansal Özet")

# -----------------------------
# Styling (Geliştirilmiş BI Standartları)
# -----------------------------
CARD_STYLE = {"borderRadius": "16px", "border": "none", "transition": "transform 0.2s"}
SECTION_CARD_CLASS = "shadow-sm mt-3"

# Net Kâr KPI kartı için daha güçlü vurgu
HIGHLIGHT_CARD_STYLE = {
    **CARD_STYLE,
    "background": "linear-gradient(145deg, #ffffff, #f0f7ff)",
    "border": "2px solid #0d6efd",
    "boxShadow": "0 10px 20px rgba(13, 110, 253, 0.15)",
}

HIGHLIGHT_BADGE_STYLE = {
    "background": "#0d6efd",
    "color": "white",
    "borderRadius": "999px",
    "padding": "2px 12px",
    "fontSize": "11px",
    "fontWeight": 800,
    "textTransform": "uppercase",
    "letterSpacing": "0.5px"
}

# IT Maliyet Modeli
ALPHA, BETA = 3157.27, 978.23

def cost_of_it(n_sellers: int, quantity: float) -> float:
    return ALPHA * (n_sellers**0.5) + BETA * (quantity**0.5)

def load_sellers():
    return Seller().get_training_data()

def brl(value: float) -> str:
    return f"{value:,.0f} BRL"

def kpi_card(title, value, subtitle="", icon="", highlight: bool = False, badge_text: str | None = None):
    style = HIGHLIGHT_CARD_STYLE if highlight else CARD_STYLE
    title_class = "fw-bold" if highlight else "text-muted fw-semibold"

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div([
                    html.Span(icon, style={"fontSize": "20px", "marginRight": "8px"}),
                    html.Span(title, className=title_class),
                    html.Span(badge_text, style=HIGHLIGHT_BADGE_STYLE, className="ms-auto") if badge_text else None,
                ], style={"display": "flex", "alignItems": "center"}),
                html.H3(brl(value), className="mt-3 mb-1 fw-bold", style={"color": "#2c3e50"}),
                html.Div(subtitle, className="text-muted small"),
            ]
        ),
        className="shadow-sm h-100",
        style=style,
    )

def build_waterfall(k):
    # Madde 3: Standardize ve Kurumsal Renkler
    COLOR_REVENUE = "#2ecc71"  # Soft Yeşil
    COLOR_COST = "#e74c3c"     # Soft Kırmızı
    COLOR_TOTAL = "#34495e"    # Kurumsal Lacivert (Ara Toplamlar için)
    COLOR_NET = "#0d6efd"      # Net Kâr için Mavi

    fig = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "total", "relative", "total", "relative", "total"],
            x=["Abonelik", "Komisyon", "Toplam Gelir", "Review", "Brüt Kâr", "IT/Oper.", "Net Kâr"],
            textposition="outside",
            # Madde 2: Etiketleri belirginleştirme
            text=[
                f"+{k['gelir_abonelik']/1e6:.1f}M",
                f"+{k['gelir_satis_komisyonu']/1e6:.1f}M",
                f"<b>{k['toplam_gelir']/1e6:.1f}M</b>",
                f"-{k['maliyet_review']/1e6:.1f}M",
                f"<b>{k['brut_kar']/1e6:.1f}M</b>",
                f"-{k['it_maliyeti']/1e6:.1f}M",
                f"<span style='font-size:16px; color:#0d6efd'><b>{k['net_kar']/1e6:.2f}M</b></span>",
            ],
            y=[k["gelir_abonelik"], k["gelir_satis_komisyonu"], 0, -k["maliyet_review"], 0, -k["it_maliyeti"], 0],
            decreasing={"marker": {"color": COLOR_COST}},
            increasing={"marker": {"color": COLOR_REVENUE}},
            totals={"marker": {"color": COLOR_TOTAL}},
            connector={"line": {"width": 1.5, "color": "#bdc3c7", "dash": "solid"}},
            hovertemplate="<b>%{x}</b><br>Tutar: %{y:,.0f} BRL<extra></extra>"
        )
    )

    fig.update_layout(
        title="<b>Gelir → Maliyet → Net Kâr Akışı</b>",
        height=520,
        margin=dict(l=40, r=40, t=100, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(size=13, family="Inter, sans-serif"),
        title_font=dict(size=24, color="#2c3e50"),
        showlegend=False
    )

    # Madde 1: Grid ve 0 Çizgisi Vurgusu
    fig.update_yaxes(
        title="BRL",
        showgrid=True,
        gridcolor="#f1f1f1",
        zeroline=True,
        zerolinewidth=3,
        zerolinecolor="#2c3e50" # 0 çizgisi artık çok net
    )

    return fig

# --- Veri Hesaplama Bölümü (Aynı Kaldı) ---
sellers = load_sellers()
gelir_satis_komisyonu = sellers["sales"].sum() * 0.10
gelir_abonelik = sellers["months_on_olist"].sum() * 80
toplam_gelir = float(sellers["revenues"].sum())
maliyet_review = float(sellers["cost_of_reviews"].sum())
n_sellers = int(sellers["seller_id"].nunique())
quantity = float(sellers["quantity"].sum())
it_maliyeti = float(cost_of_it(n_sellers, quantity))
brut_kar = float(sellers["profits"].sum())
net_kar = brut_kar - it_maliyeti

k = {
    "gelir_satis_komisyonu": float(gelir_satis_komisyonu),
    "gelir_abonelik": float(gelir_abonelik),
    "toplam_gelir": toplam_gelir,
    "maliyet_review": maliyet_review,
    "it_maliyeti": it_maliyeti,
    "brut_kar": brut_kar,
    "net_kar": net_kar,
    "n_sellers": n_sellers,
    "quantity": quantity,
}

wf_fig = build_waterfall(k)

# -----------------------------
# Layout (Geliştirilmiş İçerik)
# -----------------------------
layout = dbc.Container(
    [
        html.Div([
            html.H2("Finansal Özet — Mevcut Durum", className="mt-4 mb-1 fw-bold", style={"color": "#2c3e50"}),
            html.P("Operasyonel maliyetlerin kârlılık üzerindeki doğrudan etkisini analiz edin.", className="text-muted mb-4"),
        ]),

        dbc.Row(
            [
                dbc.Col(kpi_card("Toplam Gelir", k["toplam_gelir"], "Abonelik + Komisyon", "💰"), md=3),
                dbc.Col(kpi_card("Review Maliyeti", k["maliyet_review"], "Gecikme/İade Kaynaklı", "🧾"), md=3),
                dbc.Col(kpi_card("IT / Operasyon", k["it_maliyeti"], f"{k['n_sellers']} Satıcı Altyapısı", "🖥️"), md=3),
                dbc.Col(kpi_card("Net Kâr", k["net_kar"], "Final Operasyonel Sonuç", "📈", highlight=True, badge_text="HEDEF KPI"), md=3),
            ],
            className="g-3",
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.Div([
                        html.Span("💡 İpucu: ", className="fw-bold text-primary"),
                        "Kırmızı blokları (Review) küçültmek için teslimat süresini optimize etmek en hızlı kâr artış yoludur."
                    ], className="alert alert-light border-0 mb-0 small"),
                    dcc.Graph(figure=wf_fig, className="mt-2", config={"displayModeBar": False}),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("📌 Yönetim İçin Stratejik Notlar", className="mb-3 fw-bold", style={"color": "#2c3e50"}),
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.B("Maliyet Odağı: ", className="text-danger"),
                                "Review maliyeti 1.6M BRL ile kârı en çok baskılayan kalemdir."
                            ], className="mb-2"),
                        ], md=6),
                        dbc.Col([
                            html.Div([
                                html.B("Kâr Kaldıracı: ", className="text-success"),
                                "Düşük performanslı satıcıların yönetimi Net Kâr'ı doğrudan yukarı taşır."
                            ]),
                        ], md=6),
                    ]),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        dbc.Alert(
            [
                html.I(className="bi bi-arrow-right-circle-fill me-2"),
                html.B("Eylem Planı: "),
                "Zarar eden satıcıları simülasyondan çıkararak yeni Net Kâr potansiyelini görmek için ",
                dcc.Link("Portföy Optimizasyonu", href="/satici-etkisi", className="fw-bold text-decoration-none"),
                " sayfasına ilerleyin."
            ],
            color="info",
            className="mt-4 shadow-sm d-flex align-items-center",
            style={"borderRadius": "16px", "border": "none", "background": "rgba(13, 202, 240, 0.1)", "color": "#055160"},
        ),
    ],
    fluid=True,
    className="pb-5 px-4",
)