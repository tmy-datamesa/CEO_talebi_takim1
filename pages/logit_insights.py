# pages/logit_insights.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/memnuniyet", name="Memnuniyet Sürücüleri")

# -----------------------------
# Stil sabitleri
# -----------------------------
CARD_STYLE = {"borderRadius": "16px", "border": "none"}
SECTION_CLASS = "shadow-sm mt-4"


def load_effects() -> pd.DataFrame:
    """
    Not: Bu sayfadaki rakamlar 'standardize edilmiş' (göreli) etki gücünü temsil eder.
    Eğitimdeki logit sonuçlarından üretilmiş örnek bir özet tablo gibi düşün.
    """
    data = [
        ("Teslimat süresi (wait_time)", 0.68, 0.50),
        ("Beklenenden geç gelme (delay_vs_expected)", 0.27, 0.42),
        ("Siparişte satıcı sayısı (number_of_sellers)", 0.22, 0.18),
        ("Satıcı–müşteri uzaklığı (distance)", 0.10, 0.06),
        ("Kargo ücreti (freight_value)", 0.08, 0.05),
        ("Ürün fiyatı (price)", 0.03, 0.02),
    ]
    return pd.DataFrame(
        data,
        columns=[
            "Faktör",
            "1★ Riski Artıran Etki",
            "5★ Memnuniyeti Azaltan Etki",
        ],
    )


def _card(title: str, body: list, icon: str):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [html.Span(icon, className="me-2"), html.Span(title)],
                    className="text-muted fw-semibold",
                    style={"display": "flex", "alignItems": "center"},
                ),
                *body,
            ]
        ),
        className="shadow-sm border-0 h-100",
        style=CARD_STYLE,
    )


def build_bar(df: pd.DataFrame, col: str, title: str, color_hex: str):
    """
    col: DataFrame'deki kolon adı (ör. '1★ Riski Artıran Etki')
    title: Grafik başlığı
    """
    d = df.sort_values(col, ascending=True).copy()

    fig = px.bar(
        d,
        x=col,
        y="Faktör",
        orientation="h",
        title=title,
        text=col,
    )

    fig.update_traces(
        marker_color=color_hex,
        texttemplate="%{text:.2f}",
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_layout(
        height=420,
        margin=dict(l=20, r=30, t=55, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis_title="Göreceli Etki Gücü (standardize)",
        yaxis_title="",
        font=dict(family="Segoe UI, sans-serif"),
    )

    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.08)")
    fig.update_yaxes(tickfont=dict(size=12))
    return fig


# -----------------------------
# Data + fig
# -----------------------------
df = load_effects()

fig_1 = build_bar(
    df=df,
    col="1★ Riski Artıran Etki",
    title="▼ 1★ riskini en çok tetikleyen faktörler",
    color_hex="#EF553B",
)

fig_5 = build_bar(
    df=df,
    col="5★ Memnuniyeti Azaltan Etki",
    title="✦ 5★ memnuniyeti en çok düşüren faktörler",
    color_hex="#00CC96",
)


# En kritik başlıkları kartta göstermek için
top_1_risk = df.sort_values("1★ Riski Artıran Etki", ascending=False).iloc[0]["Faktör"]
top_5_drop = df.sort_values("5★ Memnuniyeti Azaltan Etki", ascending=False).iloc[0]["Faktör"]


# -----------------------------
# Layout
# -----------------------------
layout = dbc.Container(
    [
        html.Div(
            [
                html.H2("Müşteri Memnuniyeti — Kritik Sürücüler", className="mt-4 fw-bold"),
                html.P(
                    "Amaç: Teknik detaya girmeden, memnuniyeti en çok etkileyen operasyonel noktaları önceliklendirmek.",
                    className="text-muted",
                ),
            ]
        ),

        # Üstte 2 özet kart
        dbc.Row(
            [
                dbc.Col(
                    _card(
                        "KRİTİK RİSK NOKTASI (1★)",
                        [
                            html.H3("Teslimat Süresi", className="mt-2 mb-1 fw-bold", style={"color": "#EF553B"}),
                            html.Div(
                                "Teslimat uzadıkça düşük puan (1★) riski belirgin şekilde artıyor.",
                                className="text-muted",
                            ),
                            html.Div(
                                f"En güçlü sinyal: {top_1_risk}",
                                className="small text-muted mt-2",
                            ),
                        ],
                        "⚠️",
                    ),
                    md=6,
                ),
                dbc.Col(
                    _card(
                        "MEMNUNİYET KIRILIMI (5★)",
                        [
                            html.H3("Gecikme / Beklentinin Aşılması", className="mt-2 mb-1 fw-bold", style={"color": "#636EFA"}),
                            html.Div(
                                "Sipariş beklenenden geç geldikçe 5★ olasılığı düşüyor.",
                                className="text-muted",
                            ),
                            html.Div(
                                f"En güçlü sinyal: {top_5_drop}",
                                className="small text-muted mt-2",
                            ),
                        ],
                        "⭐",
                    ),
                    md=6,
                ),
            ],
            className="g-4",
        ),

        # Grafikler kartı
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(figure=fig_1, config={"displayModeBar": False}), md=6),
                            dbc.Col(dcc.Graph(figure=fig_5, config={"displayModeBar": False}), md=6),
                        ],
                        className="g-3",
                    ),
                ]
            ),
            className=SECTION_CLASS,
            style=CARD_STYLE,
        ),

        # Net içgörüler + Aksiyonlar
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Net içgörüler", className="mb-3 fw-bold"),
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItem("Operasyon (teslimat süresi + gecikme) memnuniyetin ana kaldıraçı.", className="border-0"),
                                        dbc.ListGroupItem("Çok satıcılı siparişler (split shipment) müşteri deneyimini zorlaştırıyor.", className="border-0"),
                                        dbc.ListGroupItem("Fiyat/kargo etkili ama operasyonel etkiler kadar belirleyici değil.", className="border-0"),
                                    ],
                                    flush=True,
                                ),
                            ]
                        ),
                        className="h-100 shadow-sm border-0",
                        style=CARD_STYLE,
                    ),
                    md=7,
                ),
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H5("Önerilen aksiyonlar", className="mb-3 fw-bold"),
                            html.Ul(
                                [
                                    html.Li("SLA hedefleri tanımla ve düzenli takip et."),
                                    html.Li("Gecikme riski için erken uyarı sistemi kur."),
                                    html.Li("Çok satıcılı siparişleri azalt/optimize et."),
                                ],
                                className="mb-0",
                            ),
                        ],
                        color="primary",
                        className="h-100 shadow-sm",
                        style={"borderRadius": "16px"},
                    ),
                    md=5,
                ),
            ],
            className="mt-4 g-4",
        ),

        # Köprü mesajı
        dbc.Alert(
            [
                html.B("Köprü mesajı: "),
                "Bu operasyonel sorunlar finansal sonuca yansıyor. Bir sonraki sayfada gelir–maliyet–net kâr özetini gösteriyoruz.",
            ],
            color="light",
            className="mt-4 shadow-sm",
            style={"borderRadius": "12px", "borderLeft": "5px solid #636EFA"},
        ),
    ],
    fluid=True,
    className="pb-5 px-4",
)
