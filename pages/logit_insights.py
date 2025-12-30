import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/memnuniyet", name="Memnuniyet Sürücüleri")

CARD_STYLE = {"borderRadius": "14px"}
SECTION_CARD_CLASS = "shadow-sm mt-3"


def load_effects() -> pd.DataFrame:
    """
    Bu değerler sizin logit çıktınızın 'sıralama' özetidir.
    İsterseniz notebook'tan kendi katsayılarınızla güncelleyebilirsiniz.

    risk_1star:
      + ise 1★ riskini artırır (mutsuzluk artar)
    impact_5star:
      - ise 5★ olasılığını düşürür (memnuniyet düşer)
    """
    data = [
        ("Teslimat süresi", 0.68, -0.50),
        ("Beklenenden geç gelme", 0.26, -0.42),
        ("Siparişte satıcı sayısı", 0.22, -0.18),
        ("Satıcı–müşteri uzaklığı", -0.22, 0.10),
        ("Kargo ücreti", 0.10, -0.06),
        ("Ürün fiyatı", 0.03, -0.02),
    ]
    return pd.DataFrame(data, columns=["factor", "risk_1star", "impact_5star"])


def kpi_card(title: str, big_text: str, subtitle: str = "", icon: str = ""):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Span(icon, style={"fontSize": "18px", "marginRight": "8px"}) if icon else None,
                        html.Span(title, className="text-muted"),
                    ],
                    style={"display": "flex", "alignItems": "center"},
                ),
                html.H3(big_text, className="mt-2 mb-1"),
                html.Div(subtitle, className="text-muted"),
            ]
        ),
        className="shadow-sm h-100",
        style=CARD_STYLE,
    )


def build_driver_chart(df: pd.DataFrame):
    # Pozitif “problem etkisi” olarak göstereceğiz:
    # - 1★ risk artışı: max(0, risk_1star)
    # - 5★ kaybı: max(0, -impact_5star)
    d = df.copy()
    d["risk_artisi_1yildiz"] = d["risk_1star"].clip(lower=0)
    d["kayıp_5yildiz"] = (-d["impact_5star"]).clip(lower=0)

    # Yönetim gözüyle: en etkili olanlar üstte kalsın
    d["toplam_etki"] = d[["risk_artisi_1yildiz", "kayıp_5yildiz"]].max(axis=1)
    d = d.sort_values("toplam_etki", ascending=True)

    long = d.melt(
        id_vars=["factor"],
        value_vars=["risk_artisi_1yildiz", "kayıp_5yildiz"],
        var_name="metric",
        value_name="value",
    )

    metric_map = {
        "risk_artisi_1yildiz": "1★ Riski (artış)",
        "kayıp_5yildiz": "5★ Memnuniyet (kayıp)",
    }
    long["metric"] = long["metric"].map(metric_map)

    fig = px.bar(
        long,
        x="value",
        y="factor",
        color="metric",
        barmode="group",
        orientation="h",
        title="Memnuniyet sürücüleri (özet sıralama)",
        labels={"value": "Etki gücü (sıralama)", "factor": "", "metric": ""},
    )
    fig.update_layout(
        height=420,
        margin=dict(l=40, r=20, t=70, b=35),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(showgrid=True, zeroline=False)
    fig.update_yaxes(tickfont=dict(size=12))
    return fig


effects = load_effects()

# KPI: en kritik 1★ risk artıran (pozitif en büyük)
top_risk = effects.sort_values("risk_1star", ascending=False).iloc[0]["factor"]
# KPI: 5★ en çok düşüren (en negatif)
top_drop5 = effects.sort_values("impact_5star", ascending=True).iloc[0]["factor"]

fig = build_driver_chart(effects)

layout = dbc.Container(
    [
        html.H2("Müşteri Memnuniyeti Sürücüleri", className="mt-4"),
        html.P(
            "Kısaca: Müşteriyi mutsuz eden (1★) ve 5★ deneyimini zayıflatan başlıca operasyonel noktalar.",
            className="text-muted",
        ),

        dbc.Row(
            [
                dbc.Col(
                    kpi_card(
                        "En kritik problem",
                        str(top_risk),
                        "Teslimat uzadıkça mutsuzluk belirgin biçimde artıyor.",
                        icon="⚠️",
                    ),
                    md=6,
                ),
                dbc.Col(
                    kpi_card(
                        "5★ deneyimini en çok bozan",
                        str(top_drop5),
                        "Sipariş beklenenden geç geldikçe 5★ olasılığı düşüyor.",
                        icon="⭐",
                    ),
                    md=6,
                ),
            ],
            className="g-3",
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        "Nasıl okunur? Çubuk uzadıkça etki güçlenir. "
                        "Bu grafik teknik bir metrik değil; önceliklendirme (hangi probleme önce odaklanalım?) içindir.",
                        className="text-muted",
                        style={"marginBottom": "10px"},
                    ),
                    dcc.Graph(figure=fig, config={"displayModeBar": False}),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Yönetim için net mesaj", className="mb-2"),
                    html.Ul(
                        [
                            html.Li("Öncelik 1: Teslimat süresini kısaltmak (SLA + izleme)."),
                            html.Li("Öncelik 2: Gecikme riskinde erken uyarı ve operasyonel müdahale."),
                            html.Li("Öncelik 3: Çok satıcılı siparişleri azaltmak / daha iyi orkestrasyon."),
                        ],
                        className="mb-0",
                    ),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        dbc.Alert(
            [
                html.B("Köprü: "),
                "Bu operasyonel sorunların finansal karşılığı var. Bir sonraki sayfada bunu gelir–maliyet–net kâr kırılımıyla gösteriyoruz.",
            ],
            color="primary",
            className="mt-3",
            style={"borderRadius": "12px"},
        ),
    ],
    fluid=True,
)
