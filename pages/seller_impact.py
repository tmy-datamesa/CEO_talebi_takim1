import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from olist.seller_updated import Seller

dash.register_page(__name__, path="/seller-impact", name="Seller Impact")

alpha, beta = 3157.27, 978.23  # notebook’taki parametreler

def cost_of_it(df, alpha, beta):
    # df içinde n_sellers ve quantity bekleniyor
    return alpha * (df["n_sellers"] ** 0.5) + beta * (df["quantity"] ** 0.5)

def prepare_metrics():
    sellers = Seller().get_training_data()

    metrics_ordered = (
        sellers[["revenues", "cost_of_reviews", "profits", "quantity"]]
        .sort_values(by="profits", ascending=False)
        .reset_index(drop=True)
    )
    metrics_ordered["cost_of_reviews"] *= -1
    metrics_ordered["n_sellers"] = 1

    metrics_cum = metrics_ordered.cumsum()

    metrics_cum_it = metrics_ordered.cumsum()
    metrics_cum_it["it_costs"] = -cost_of_it(metrics_cum_it, alpha, beta)
    metrics_cum_it["profits_after_it"] = metrics_cum_it["profits"] + metrics_cum_it["it_costs"]

    opt_without_it = int(metrics_cum["profits"].idxmax())
    opt_with_it = int(metrics_cum_it["profits_after_it"].idxmax())

    return sellers, metrics_ordered, metrics_cum, metrics_cum_it, opt_without_it, opt_with_it

sellers_df, metrics_ordered, metrics_cum, metrics_cum_it, opt_wo, opt_w = prepare_metrics()
max_remove = len(metrics_ordered) - 1

def cumulative_profit_figure(metrics_cum, metrics_cum_it, opt_wo, opt_w):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=metrics_cum.index, y=metrics_cum["profits"], name="Profit (no IT)"))
    fig.add_trace(go.Scatter(x=metrics_cum_it.index, y=metrics_cum_it["profits_after_it"], name="Profit (after IT)"))

    fig.add_vline(x=opt_wo, line_dash="dash", annotation_text="Best no-IT", annotation_position="top left")
    fig.add_vline(x=opt_w, line_dash="dash", annotation_text="Best after-IT", annotation_position="top right")

    fig.update_layout(
        title="Cumulative Profit vs Number of Sellers Kept (sorted by profit)",
        xaxis_title="Number of sellers kept (cumulative index)",
        yaxis_title="Profit",
        height=450,
        margin=dict(l=30, r=30, t=60, b=30),
    )
    return fig

base_line_fig = cumulative_profit_figure(metrics_cum, metrics_cum_it, opt_wo, opt_w)

layout = dbc.Container(
    [
        html.H2("Seller Removal Impact", className="mt-4"),
        html.P(
            "Slider ile kaç seller’ı çıkardığında (en kötüden başlayarak) kârın nasıl değiştiğini göster.",
            className="text-muted",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div("Remove worst sellers (count)"),
                                dcc.Slider(
                                    id="remove_n",
                                    min=0,
                                    max=max_remove,
                                    step=1,
                                    value=min(200, max_remove),
                                    tooltip={"placement": "bottom", "always_visible": False},
                                ),
                                html.Div(id="remove_summary", className="mt-2 text-muted"),
                            ]
                        ),
                        className="shadow-sm",
                    ),
                    md=12,
                )
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([dcc.Graph(id="cum_profit_graph", figure=base_line_fig)]),
                        className="shadow-sm mt-3",
                    ),
                    md=8,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([dcc.Graph(id="impact_barh")]),
                        className="shadow-sm mt-3",
                    ),
                    md=4,
                ),
            ],
            className="g-3",
        ),
    ],
    fluid=True,
)

@dash.callback(
    Output("remove_summary", "children"),
    Output("impact_barh", "figure"),
    Input("remove_n", "value"),
)
def update_impact(remove_n):
    # remove_n: en kötüden kaç seller çıkarılıyor?
    # metrics_ordered: en iyiden en kötüye sıralı, bu yüzden sondan kırpacağız
    kept = metrics_ordered.iloc[: max_remove - remove_n]

    # yeni kümülatif (kept üzerinden)
    cum = kept[["revenues", "cost_of_reviews", "profits", "quantity"]].copy()
    cum["n_sellers"] = 1
    cum = cum.cumsum()
    cum["it_costs"] = -cost_of_it(cum, alpha, beta)
    cum["profits_after_it"] = cum["profits"] + cum["it_costs"]

    # özet KPI
    profit_no_it = float(cum["profits"].iloc[-1]) if len(cum) else 0.0
    profit_after_it = float(cum["profits_after_it"].iloc[-1]) if len(cum) else 0.0

    summary = f"Removed: {remove_n} | Kept: {len(kept)} | Profit(no IT): {profit_no_it:,.0f} | Profit(after IT): {profit_after_it:,.0f}"

    # barh: kept sonrası basit P&L kırılımı (toplam)
    revenues_total = float(cum["revenues"].iloc[-1]) if len(cum) else 0.0
    review_costs = float(cum["cost_of_reviews"].iloc[-1]) if len(cum) else 0.0
    it_costs = float(cum["it_costs"].iloc[-1]) if len(cum) else 0.0

    impact = pd.Series(
        {
            "Revenues": revenues_total,
            "Reviews Cost": review_costs,
            "IT Cost": it_costs,
            "Profit after IT": profit_after_it,
        }
    ).sort_values()

    fig = px.bar(
        impact,
        orientation="h",
        title="P&L snapshot (kept sellers)",
    )
    fig.update_layout(height=450, margin=dict(l=20, r=20, t=60, b=30))

    return summary, fig
