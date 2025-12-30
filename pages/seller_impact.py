import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Veri çekme sınıfınızı içe aktarın
from olist.seller_updated import Seller

# Sayfa Kaydı
dash.register_page(__name__, path="/satici-etkisi", name="Satıcı Çıkarma Etkisi")

# -----------------------------
# Styling helpers
# -----------------------------
CARD_STYLE = {"borderRadius": "14px"}
SECTION_CARD_CLASS = "shadow-sm mt-3"

def brl(x: float) -> str:
    return f"{x:,.0f} BRL"

def kpi_card(title: str, value: str, subtitle: str = "", icon: str = ""):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Span(icon, style={"fontSize": "18px", "marginRight": "8px"}) if icon else None,
                        html.Span(title, className="text-muted fw-semibold"),
                    ],
                    style={"display": "flex", "alignItems": "center"},
                ),
                html.H3(value, className="mt-2 mb-1 fw-bold"),
                html.Div(subtitle, className="text-muted"),
            ]
        ),
        className="shadow-sm h-100",
        style=CARD_STYLE,
    )

# -----------------------------
# Data load
# -----------------------------
try:
    SELLERS_DF = Seller().get_training_data().copy()
except Exception:
    SELLERS_DF = pd.DataFrame(columns=["seller_id", "revenues", "cost_of_reviews", "quantity", "profits"])

SELLERS_DF["gross_profit"] = SELLERS_DF["revenues"] - SELLERS_DF["cost_of_reviews"]
SELLERS_ASC = SELLERS_DF.sort_values("gross_profit", ascending=True).reset_index(drop=True)
SELLERS_DESC = SELLERS_DF.sort_values("gross_profit", ascending=False).reset_index(drop=True)
TOTAL_SELLERS = int(SELLERS_DF["seller_id"].nunique()) if not SELLERS_DF.empty else 0

# -----------------------------
# IT cost (Geliştirilmiş Model)
# -----------------------------
ALPHA, BETA = 3157.27, 978.23

def compute_it_cost(n_sellers: int, n_items: int) -> float:
    return ALPHA * np.sqrt(n_sellers) + BETA * np.sqrt(n_items)

def scenario_totals(df: pd.DataFrame) -> dict:
    n_sellers = int(df["seller_id"].nunique())
    n_items = int(df["quantity"].sum())
    revenue = float(df["revenues"].sum())
    review_cost = float(df["cost_of_reviews"].sum())
    gross_profit = float(df["gross_profit"].sum())
    it_cost = float(compute_it_cost(n_sellers, n_items))
    net_profit = gross_profit - it_cost
    return {
        "n_sellers": n_sellers, "n_items": n_items, "revenue": revenue,
        "review_cost": review_cost, "gross_profit": gross_profit,
        "it_cost": it_cost, "net_profit": net_profit,
    }

BASE = scenario_totals(SELLERS_DF) if not SELLERS_DF.empty else {}

# -----------------------------
# İdeal Nokta Hesaplama (Optimization)
# -----------------------------
def find_optimal_point():
    """Kârı maksimize eden noktayı önceden hesaplar"""
    profits = []
    # Performans için her 10 satıcıda bir örnekle (isteğe bağlı hassaslaştırılabilir)
    for i in range(0, TOTAL_SELLERS, 10):
        test_df = SELLERS_ASC.iloc[i:]
        res = scenario_totals(test_df)
        profits.append((i, res["net_profit"]))
    
    if not profits: return 0, 0
    best_remove, best_val = max(profits, key=lambda x: x[1])
    return best_remove, best_val

BEST_REMOVE_N, BEST_NET_VAL = find_optimal_point()

# -----------------------------
# Figures
# -----------------------------
def build_profit_curve_fig(kept_count: int):
    tmp = SELLERS_DESC.copy()
    tmp["cum_sellers"] = range(1, len(tmp) + 1)
    tmp["cum_items"] = tmp["quantity"].cumsum()
    tmp["cum_gross_profit"] = tmp["revenues"].cumsum() - tmp["cost_of_reviews"].cumsum()
    tmp["cum_it_cost"] = tmp.apply(lambda r: compute_it_cost(int(r["cum_sellers"]), int(r["cum_items"])), axis=1)
    tmp["cum_net_profit"] = tmp["cum_gross_profit"] - tmp["cum_it_cost"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tmp["cum_sellers"], y=tmp["cum_gross_profit"], mode="lines", name="Kâr (IT hariç)", line=dict(color="#6c757d")))
    fig.add_trace(go.Scatter(x=tmp["cum_sellers"], y=tmp["cum_net_profit"], mode="lines", name="Net Kâr (IT dahil)", line=dict(color="#0d6efd")))
    
    # İdeal Nokta Yıldızı
    fig.add_trace(go.Scatter(
        x=[TOTAL_SELLERS - BEST_REMOVE_N], 
        y=[BEST_NET_VAL],
        mode="markers",
        marker=dict(symbol="star", size=15, color="gold", line=dict(width=1, color="black")),
        name="İdeal Nokta (Peak Profit)"
    ))

    fig.add_vline(x=kept_count, line_width=2, line_dash="dash", line_color="red")
    
    fig.update_layout(
        title="📈 Portföy Boyutu vs Kârlılık",
        height=400, margin=dict(l=20, r=20, t=60, b=40),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.1, x=0.02)
    )
    return fig

def build_pl_snapshot_fig(totals: dict):
    dfp = pd.DataFrame({
        "Kalem": ["Gelir", "Review", "IT/Oper.", "Net Kâr"],
        "Tutar": [totals["revenue"], -totals["review_cost"], -totals["it_cost"], totals["net_profit"]],
    })
    fig = px.bar(dfp, x="Tutar", y="Kalem", orientation="h", text="Tutar", color="Kalem",
                 color_discrete_map={"Gelir": "#2ecc71", "Review": "#e74c3c", "IT/Oper.": "#e67e22", "Net Kâr": "#3498db"})
    fig.update_traces(texttemplate="%{text:,.0s} BRL", textposition="outside")
    fig.update_layout(showlegend=False, height=400, margin=dict(l=10, r=60, t=40, b=40),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig

# -----------------------------
# Layout
# -----------------------------
layout = dbc.Container([
    html.H2("Satıcı Çıkarma Etkisi — Senaryo Analizi", className="mt-4 mb-1 fw-bold"),
    html.P("Net kârı aşağı çeken satıcıları tespit edip portföyü optimize edin.", className="text-muted mb-3"),

    # İdeal Senaryo Rozeti
    dbc.Alert([
        html.Div([
            html.I(className="bi bi-graph-up-arrow me-2"),
            html.B("Optimum Senaryo: "),
            f"En düşük performanslı {BEST_REMOVE_N} satıcı çıkarıldığında Net Kâr ",
            html.B(brl(BEST_NET_VAL)), " seviyesine ulaşarak maksimize ediliyor."
        ])
    ], color="primary", className="shadow-sm border-0 mb-3", style={"borderRadius": "12px"}),

    dbc.Card(dbc.CardBody([
        html.Div("🎛️ Senaryo: En düşük performanslı kaç satıcıyı portföyden çıkaralım?", className="text-muted small"),
        dcc.Slider(
            id="remove_sellers", min=0, max=TOTAL_SELLERS, step=1, value=0,
            tooltip={"placement": "bottom", "always_visible": True},
            marks={0: '0', BEST_REMOVE_N: {'label': 'İDEAL', 'style': {'color': '#0d6efd', 'fontWeight': 'bold'}}, TOTAL_SELLERS: str(TOTAL_SELLERS)}
        ),
        html.Div(id="scenario_line", className="text-center mt-2 fw-bold text-primary")
    ]), className="shadow-sm border-0 mb-3", style=CARD_STYLE),

    dbc.Row(id="kpi_row", className="g-3 mb-3"),

    dbc.Row([
        dbc.Col(dcc.Graph(id="profit_curve", config={"displayModeBar": False}), md=7),
        dbc.Col(dcc.Graph(id="pl_snapshot", config={"displayModeBar": False}), md=5),
    ]),

    # Stratejik Notlar Bölümü
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody([
                html.H5("📌 Stratejik Yönetim Notları", className="fw-bold mb-3"),
                html.Ul([
                    html.Li([html.B("Operasyonel Yük: "), "Zarar eden satıcılar sadece ciro kaybı değil, yüksek 'Review' maliyeti ile Net Kâr'ı eritiyor."]),
                    html.Li([html.B("Ölçek Ekonomisi: "), "IT maliyetleri satıcı sayısı ile doğrusal değil, karekök oranında azalıyor."]),
                    html.Li([html.B("Altın Oran: "), f"Portföyün %{(BEST_REMOVE_N/TOTAL_SELLERS)*100:.1f} kadarını temizlemek teknik olarak en kârlı noktadır."]),
                ])
            ]), className="shadow-sm border-0 mt-3", style=CARD_STYLE),
            md=12
        )
    ]),

    dbc.Alert(
        "💡 İpucu: Eğrinin tepe noktası (yıldız), lojistik maliyetlerin ve gelirin optimize olduğu ideal satıcı sayısını gösterir.",
        color="info", className="mt-3 shadow-sm border-0", style={"borderRadius": "12px"}
    )
], fluid=True)

# -----------------------------
# Callback
# -----------------------------
@dash.callback(
    Output("profit_curve", "figure"),
    Output("pl_snapshot", "figure"),
    Output("scenario_line", "children"),
    Output("kpi_row", "children"),
    Input("remove_sellers", "value"),
)
def update_scenario(remove_n):
    if remove_n is None: remove_n = 0
    
    kept_df = SELLERS_ASC.iloc[int(remove_n):].copy()
    totals = scenario_totals(kept_df)
    
    kept_count = totals["n_sellers"]
    removed_count = TOTAL_SELLERS - kept_count
    
    fig_left = build_profit_curve_fig(kept_count)
    fig_right = build_pl_snapshot_fig(totals)
    
    delta = totals["net_profit"] - BASE["net_profit"]
    delta_txt = f"{'+' if delta >= 0 else ''}{brl(delta)}"
    
    scenario_text = f"🧹 {removed_count} satıcı çıkarıldı | 📈 Yeni Net Kâr: {brl(totals['net_profit'])}"
    
    kpis = [
        dbc.Col(kpi_card("Çıkarılan", f"{removed_count}", "En kötü performanslı", "🧹"), md=3),
        dbc.Col(kpi_card("Kalan", f"{kept_count}", "Aktif satıcı sayısı", "🏪"), md=3),
        dbc.Col(kpi_card("Net Kâr", brl(totals["net_profit"]), "Simüle edilen durum", "📈"), md=3),
        dbc.Col(kpi_card("Değişim", delta_txt, "Baz duruma kıyasla", "🧭"), md=3),
    ]
    
    return fig_left, fig_right, scenario_text, kpis