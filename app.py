import dash
from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.MORPH],
    suppress_callback_exceptions=True,
)

# Net menü sırası (storytelling)
NAV_ITEMS = [
    ("Memnuniyet Sürücüleri", "/memnuniyet"),
    ("CEO Özeti", "/"),
    ("Satıcı Çıkarma Etkisi", "/satici-etkisi"),
    ("Hakkında", "/hakkinda"),
]

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("Olist CEO Talebi Dashboard", href="/"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink(label, href=path, active="exact"))
                    for label, path in NAV_ITEMS
                ],
                className="ms-auto",
                navbar=True,
                pills=True,
            ),
        ]
    ),
    color="primary",
    dark=True,
    className="shadow-sm",
)

app.layout = html.Div(
    [
        navbar,
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
