import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about", name="About")

layout = dbc.Container(
    [
        html.H2("What to tell the CEO", className="mt-4"),
        html.Ul(
            [
                html.Li("Problem: bazı seller’lar net kârı aşağı çekiyor."),
                html.Li("Approach: seller’ları kâra göre sıralayıp en kötüleri çıkarmanın etkisini simüle ediyoruz."),
                html.Li("Decision: IT maliyeti dahil/dahil değil senaryoları ile optimum noktayı gösteriyoruz."),
            ]
        ),
    ],
    fluid=True,
)
