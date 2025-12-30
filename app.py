import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

# BI görünüm: daha “kurumsal + modern” bir tema
THEME = dbc.themes.FLATLY  # MORPH yerine daha dashboard hissi verir

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[THEME],
    suppress_callback_exceptions=True,
)

# Net menü sırası (storytelling)
NAV_ITEMS = [
    ("📌 Memnuniyet Sürücüleri", "/memnuniyet"),
    ("💼 CEO Özeti", "/"),
    ("🧩 Satıcı Çıkarma Etkisi", "/satici-etkisi"),
    ("ℹ️ Hakkında", "/hakkinda"),
]

BRAND_STYLE = {
    "fontWeight": "700",
    "letterSpacing": "0.2px",
}

navbar = dbc.Navbar(
    dbc.Container(
        [
            # Sol taraf: marka
            dbc.NavbarBrand(
                html.Span(
                    ["📊 ", html.Span("Olist", style={"fontWeight": "800"}), " | Yönetim İçgörü Paneli"],
                    style=BRAND_STYLE,
                ),
                href="/",
                className="me-3",
            ),

            # Sağ taraf: menü (pills)
            dbc.Nav(
                [
                    dbc.NavItem(
                        dbc.NavLink(
                            label,
                            href=path,
                            active="exact",
                            className="px-3",
                            style={"borderRadius": "12px"},
                        )
                    )
                    for label, path in NAV_ITEMS
                ],
                className="ms-auto",
                navbar=True,
                pills=True,
                style={
                    "background": "rgba(255,255,255,0.18)",
                    "padding": "8px",
                    "borderRadius": "14px",
                    "backdropFilter": "blur(6px)",
                },
            ),
        ],
        fluid=True,
        style={"maxWidth": "1200px"},
    ),
    color="primary",
    dark=True,
    className="shadow-sm",
    style={"height": "72px"},
)

# BI standardı: sayfa içeriğini ortala + boşlukları sabitle
app.layout = html.Div(
    [
        navbar,
        html.Div(
            dash.page_container,
            style={
                "maxWidth": "1200px",
                "margin": "0 auto",
                "padding": "18px 16px 36px 16px",
            },
        ),
    ],
    style={"backgroundColor": "#f4f6fb", "minHeight": "100vh"},
)

if __name__ == "__main__":
    app.run(debug=True)
