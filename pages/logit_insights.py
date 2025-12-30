import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/memnuniyet", name="Memnuniyet Sürücüleri")

CARD_STYLE = {"borderRadius": "14px"}

# Burada siz kendi notebook çıktınıza göre bu tabloyu dolduruyordunuz.
# Bu örnekte; "etki" değerleri (coef) temsili gibi duruyor: sizde zaten hazırsa aynen bağlayın.
def load_effects() -> pd.DataFrame:
    # feature, risk_1star (sağa), satisfaction_5star (sola)
    data = [
        ("Teslimat süresi", 0.68, -0.50),
        ("Beklenenden geç gelme", 0.25, -0.42),
        ("Siparişte satıcı sayısı", 0.22, -0.18),
        ("Satıcı–müşteri uzaklığı", -0.21, 0.10),
        ("Kargo ücreti", 0.10, -0.06),
        ("Ürün fiyatı", 0.04, -0.02),
    ]
    df = pd.DataFrame(data, columns=["Faktör", "Mutsuzluk Riski (1★)", "Memnuniyet (5★)"])
    return df

def build_bar(df: pd.DataFrame):
    long = df.melt(id_vars="Faktör", var_name="Tür", value_name="Etki")
    fig = px.bar(
        long,
        y="Faktör",
        x="Etki",
        color="Tür",
        orientation="h",
        title="Sipariş Deneyimini Etkileyen Unsurlar",
    )
    fig.update_layout(
        height=420,
        margin=dict(l=30, r=30, t=70, b=30),
        legend_title_text="",
    )
    fig.update_yaxes(title="")
    fig.update_xaxes(title="Etki")
    return fig

effects = load_effects()
fig = build_bar(effects)

layout = dbc.Container(
    [
        html.H2("Müşteri Memnuniyetini Etkileyen Faktörler", className="mt-4"),
        html.P(
            "Sipariş deneyiminde hangi unsurlar müşteriyi mutsuz ediyor, hangileri memnuniyeti artırıyor?",
            className="text-muted",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div("⚠️  Müşteriyi en çok mutsuz eden faktör", className="text-muted"),
                                html.H3("Teslimat Süresi", className="mt-2"),
                                html.Div(
                                    "Teslimat süresi uzadıkça 1 yıldızlı yorum ihtimali belirgin şekilde artıyor.",
                                    className="text-muted",
                                ),
                            ]
                        ),
                        className="shadow-sm",
                        style=CARD_STYLE,
                    ),
                    md=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div("⭐  5 yıldızlı deneyimi en çok zayıflatan faktör", className="text-muted"),
                                html.H3("Gecikme ve beklentinin aşılması", className="mt-2"),
                                html.Div(
                                    "Sipariş beklenenden geç geldikçe 5 yıldızlı yorum ihtimali düşüyor.",
                                    className="text-muted",
                                ),
                            ]
                        ),
                        className="shadow-sm",
                        style=CARD_STYLE,
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
                        "Nasıl okunur? Sağa uzayan çubuklar mutsuzluk riskini artırır, sola uzayanlar memnuniyeti destekler.",
                        className="text-muted",
                    ),
                    dcc.Graph(figure=fig, className="mt-2"),
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
                            html.Li("Teslimat süresi ve gecikme arttıkça memnuniyetsizlik yükseliyor."),
                            html.Li("Çok satıcılı siparişler daha fazla sorun yaratıyor."),
                            html.Li("Fiyatın etkisi, operasyonel faktörlere kıyasla daha sınırlı."),
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
                html.B("Köprü mesajı: "),
                "Bu operasyonel sorunların finansal bir karşılığı var. Bir sonraki sayfada mevcut kâr kırılımını (gelir–maliyet–net kâr) özetliyoruz.",
            ],
            color="primary",
            className="mt-3",
            style={"borderRadius": "12px"},
        ),
    ],
    fluid=True,
)
