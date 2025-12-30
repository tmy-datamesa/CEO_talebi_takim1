# pages/about.py
import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about", name="Hakkında")

CARD_STYLE = {"borderRadius": "14px"}
SECTION_CARD_CLASS = "shadow-sm mt-3"


layout = dbc.Container(
    [
        html.H2("Hakkında", className="mt-4"),
        html.P(
            "Bu dashboard, Olist veri setinden yola çıkarak kârlılığı ve müşteri memnuniyetini etkileyen ana faktörleri "
            "yönetim seviyesinde (CEO diliyle) özetlemek için hazırlanmıştır.",
            className="text-muted",
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Bu dashboard neyi cevaplıyor?", className="mb-2"),
                    html.Ul(
                        [
                            html.Li("Mevcut durumda gelir–maliyet–net kâr dengemiz nasıl?"),
                            html.Li("Zarar eden satıcıları çıkarmak net kârı artırır mı, hangi noktada en iyi sonuç oluşur?"),
                            html.Li("Müşteri memnuniyetini en çok etkileyen operasyonel faktörler neler?"),
                        ],
                        className="mb-0",
                    ),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Varsayımlar (basit ve şeffaf)", className="mb-2"),
                    html.Ul(
                        [
                            html.Li("Gelir: Abonelik + satış komisyonu (satışların %10’u)."),
                            html.Li("Review maliyeti: Düşük puanlı yorumların operasyonel maliyet yarattığı varsayımıyla hesaplanır."),
                            html.Li("IT/Operasyon maliyeti: Satıcı ve ürün hacmine göre ölçeklenen basit bir maliyet modeli (eğitim senaryosu)."),
                        ],
                        className="mb-0",
                    ),
                    dbc.Alert(
                        "Not: Bu çalışma eğitim amaçlıdır. Maliyet kalemleri gerçek şirket verisi değildir; amaç, karar destek yaklaşımını göstermektir.",
                        color="info",
                        className="mt-3",
                        style={"borderRadius": "12px"},
                    ),
                ]
            ),
            className=SECTION_CARD_CLASS,
            style=CARD_STYLE,
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Sayfalar nasıl okunur?", className="mb-2"),
                    html.Ul(
                        [
                            html.Li("Özet (CEO): Mevcut durumun gelir–maliyet–net kâr özeti."),
                            html.Li("Satıcı Çıkarma Etkisi: En düşük performanslı satıcıları çıkardığımız senaryolarda net kârın değişimi."),
                            html.Li("Müşteri Memnuniyetini Etkileyen Faktörler: Memnuniyeti artıran / mutsuzluğu artıran operasyonel unsurlar ve önerilen aksiyonlar."),
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
                html.B("Sunum odağı: "),
                "Kod değil; içgörü ve aksiyon. Bu dashboard, yönetime “ne yapmalıyız?” sorusunun kısa cevabını vermeyi hedefler.",
            ],
            color="primary",
            className="mt-3",
            style={"borderRadius": "12px"},
        ),
    ],
    fluid=True,
)
