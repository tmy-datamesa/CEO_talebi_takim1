import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from olist.seller_updated import Seller

dash.register_page(__name__, path="/", name="Home")

def load_sellers():
    seller = Seller()
    sellers = seller.get_training_data()
    return sellers

def build_kpis(sellers):
    revenues_sales = sellers.sales.sum() * 0.10
    revenues_subscription = sellers.months_on_olist.sum() * 80
    revenues_total = sellers.revenues.sum()

    costs_reviews = sellers.cost_of_reviews.sum()
    costs_it = 500_000  # notebook’taki varsayım
    profits_gross = sellers.profits.sum()
    profits_net = profits_gross - costs_it

    return {
        "revenues_sales": revenues_sales,
        "revenues_subscription": revenues_subscription,
        "revenues_total": revenues_total,
        "costs_reviews": costs_reviews,
        "costs_it": costs_it,
        "profits_gross": profits_gross,
        "profits_net": profits_net,
    }

def build_waterfall(k):
    fig = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "total", "relative", "total", "relative", "total"],
            x=[
                "Monthly subscriptions",
                "Sales fees",
                "Total Revenues",
                "Reviews costs",
                "Gross Profit",
                "IT costs",
                "Net Profit",
            ],
            y=[
                k["revenues_subscription"],
                k["revenues_sales"],
                0,
                -k["costs_reviews"],
                0,
                -k["costs_it"],
                0,
            ],
        )
    )
    fig.update_layout(
        title="Olist Profit & Loss (BRL)",
        margin=dict(l=30, r=30, t=60, b=30),
        height=450,
    )
    return fig

sellers_df = load_sellers()
k = build_kpis(sellers_df)
wf_fig = build_waterfall(k)

def kpi_card(title, value, subtitle=None):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted"),
                html.H3(f"{value:,.0f} BRL"),
                html.Div(subtitle or "", className="text-muted"),
            ]
        ),
        className="shadow-sm",
    )

layout = dbc.Container(
    [
        html.H2("CEO Summary", className="mt-4"),
        html.P(
            "Amaç: kârlılığı artırmak için (özellikle negatif kârlı) seller’ların etkisini göstermek.",
            className="text-muted",
        ),
        dbc.Row(
            [
                dbc.Col(kpi_card("Total Revenues", k["revenues_total"], "Subscription + Sales fee"), md=3),
                dbc.Col(kpi_card("Reviews Cost", k["costs_reviews"], "Maliyet kalemi"), md=3),
                dbc.Col(kpi_card("IT Cost (assumption)", k["costs_it"], "Sabit varsayım"), md=3),
                dbc.Col(kpi_card("Net Profit", k["profits_net"], "Gross - IT"), md=3),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("P&L Waterfall", className="mb-2"),
                                dcc.Graph(figure=wf_fig),
                            ]
                        ),
                        className="shadow-sm mt-3",
                    ),
                    md=12,
                )
            ]
        ),
    ],
    fluid=True,
)
