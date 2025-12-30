import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

from olist.seller_updated import Seller

dash.register_page(__name__, path="/", name="CEO Özeti")

CARD_STYLE = {"borderRadius": "14px"}

# Seller Impact ile aynı IT maliyeti modeli (senkron olsun diye)
ALPHA, BETA = 3157.27, 978.23

def cost_of_it(n_sellers: int, quantity: float) -> float:
    return ALPHA * (n_sellers ** 0.5) + BETA * (quantity ** 0.5)

def load_sellers():
    return Seller().get_training_data()

def tl(value):
    return f"{value:,.0f} BRL"

def kpi_card(title, value, subtitle="", icon=""):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(f"{icon}  {title}".strip(), className="text-muted"),
                html.H3(tl(value), className="mt-1"),
                html.Div(subtitle, className="text-muted"),
            ]
        ),
        className="shadow-sm",
        style=CARD_STYLE,
    )

def build_waterfall(k):
    fig = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "total", "relative", "total", "relative", "total"],
            x=[
                "Aylık Abonelik",
                "Satış Komisyonu",
                "Toplam Gelir",
                "Review Maliyeti",
                "Brüt Kâr",
                "IT Maliyeti",
                "Net Kâr",
            ],
            y=[
                k["gelir_abonelik"],
                k["gelir_satis_komisyonu"],
                0,
                -k["maliyet_review"],
                0,
                -k["it_maliyeti"],
                0,
            ],
        )
    )
    fig.update_layout(
        title="Gelir–Maliyet Akışı",
        margin=dict(l=30, r=30, t=60, b=30),
        height=460,
    )
    return fig

sellers = load_sellers()

gelir_satis_komisyonu = sellers["sales"].sum() * 0.10
gelir_abonelik = sellers["months_on_olist"].sum() * 80
toplam_gelir = sellers["revenues"].sum()

maliyet_review = sellers["cost_of_reviews"].sum()

n_sellers = int(sellers["seller_id"].nunique())
quantity = float(sellers["quantity"].sum())
it_maliyeti = cost_of_it(n_sellers, quantity)

brut_kar = sellers["profits"].sum()
net_kar = brut_kar - it_maliyeti

k = {
    "gelir_satis_komisyonu": gelir_satis_komisyonu,
    "gelir_abonelik": gelir_abonelik,
    "toplam_gelir": toplam_gelir,
    "maliyet_review": maliyet_review,
    "it_maliyeti": it_maliyeti,
    "brut_kar": brut_kar,
    "net_kar": net_kar,
    "n_sellers": n_sellers,
    "quantity": quantity,
}

wf_fig = build_waterfall(k)

layout = dbc.Container(
    [
        html.H2("CEO Özeti", className="mt-4"),
        html.P(
            "Bu sayfa mevcut durumu (hiç satıcı çıkarmadan) gelir–maliyet–kâr kırılımıyla özetler.",
            className="text-muted",
        ),

        dbc.Row(
            [
                dbc.Col(kpi_card("Toplam Gelir", k["toplam_gelir"], "Abonelik + Komisyon", "💰"), md=3),
                dbc.Col(kpi_card("Review Maliyeti", k["maliyet_review"], "Memnuniyetsizliğin finansal yükü", "🧾"), md=3),
                dbc.Col(kpi_card("IT / Operasyon Maliyeti", k["it_maliyeti"], f"{k['n_sellers']} satıcı • {int(k['quantity']):,} ürün (varsayım)", "🖥️"), md=3),
                dbc.Col(kpi_card("Net Kâr", k["net_kar"], "Brüt Kâr - IT", "📈"), md=3),
            ],
            className="g-3",
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        "Nasıl okunur? Yeşil bloklar geliri, kırmızı bloklar maliyetleri gösterir. En sağdaki Net Kâr, tüm gelirlerden tüm maliyetler çıktıktan sonra kalan tutardır.",
                        className="text-muted",
                    ),
                    dcc.Graph(figure=wf_fig, className="mt-2"),
                ]
            ),
            className="shadow-sm mt-3",
            style=CARD_STYLE,
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Özet çıkarımlar", className="mb-2"),
                    html.Ul(
                        [
                            html.Li("Gelirin ana kaynağı: abonelik ve satış komisyonu."),
                            html.Li("En büyük maliyet kalemi: review maliyeti (memnuniyetsizlik)."),
                            html.Li("Net kârı artırmak için iki kaldıraç var: operasyonel gecikmeleri azaltmak ve zarar eden satıcıları yönetmek."),
                        ],
                        className="mb-0",
                    ),
                ]
            ),
            className="shadow-sm mt-3",
            style=CARD_STYLE,
        ),

        dbc.Alert(
            [
                html.B("Sonraki adım: "),
                "“Satıcı Çıkarma Etkisi” sayfasında, en düşük performanslı satıcıları çıkardığımızda net kârın nasıl değiştiğini senaryo bazlı inceleyebilirsiniz.",
            ],
            color="primary",
            className="mt-3",
            style={"borderRadius": "12px"},
        ),
    ],
    fluid=True,
)
