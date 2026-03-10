# import pandas as pd
# import plotly.express as px

# from data_processor import load_deals_dataframe, load_work_orders_dataframe


# # =========================
# # BUSINESS INSIGHTS
# # =========================

# def get_total_pipeline_value(deals_df):
#     return float(deals_df["Masked Deal value"].sum())


# def get_pipeline_by_sector(deals_df):
#     sector_pipeline = (
#         deals_df.groupby("Sector/service")["Masked Deal value"]
#         .sum()
#         .sort_values(ascending=False)
#     )
#     return sector_pipeline


# def get_deals_by_stage(deals_df):
#     return deals_df["Deal Stage"].value_counts()


# def get_deals_by_probability(deals_df):
#     return deals_df["Closure Probability"].value_counts()


# def get_work_order_execution_status(work_orders_df):
#     return work_orders_df["Execution Status"].value_counts()


# def get_revenue_by_sector(work_orders_df):

#     if "Amount in Rupees (Excl of GST) (Masked)" not in work_orders_df.columns:
#         return None

#     revenue_sector = (
#         work_orders_df.groupby("Sector")["Amount in Rupees (Excl of GST) (Masked)"]
#         .sum()
#         .sort_values(ascending=False)
#     )

#     return revenue_sector


# # =========================
# # GRAPH FUNCTIONS
# # =========================

# def pipeline_sector_chart(deals_df):

#     data = (
#         deals_df.groupby("Sector/service")["Masked Deal value"]
#         .sum()
#         .reset_index()
#     )

#     fig = px.bar(
#         data,
#         x="Sector/service",
#         y="Masked Deal value",
#         title="Pipeline Value by Sector",
#         color="Sector/service"
#     )

#     return fig


# def deals_stage_chart(deals_df):

#     data = deals_df["Deal Stage"].value_counts().reset_index()
#     data.columns = ["Stage", "Count"]

#     fig = px.bar(
#         data,
#         x="Stage",
#         y="Count",
#         title="Deals by Stage",
#         color="Stage"
#     )

#     return fig


# def deals_probability_chart(deals_df):

#     data = deals_df["Closure Probability"].value_counts().reset_index()
#     data.columns = ["Probability", "Count"]

#     fig = px.pie(
#         data,
#         names="Probability",
#         values="Count",
#         title="Deal Closure Probability Distribution"
#     )

#     return fig


# def execution_status_chart(work_orders_df):

#     data = work_orders_df["Execution Status"].value_counts().reset_index()
#     data.columns = ["Status", "Count"]

#     fig = px.bar(
#         data,
#         x="Status",
#         y="Count",
#         title="Work Order Execution Status",
#         color="Status"
#     )

#     return fig


# def revenue_sector_chart(work_orders_df):

#     if "Amount in Rupees (Excl of GST) (Masked)" not in work_orders_df.columns:
#         return None

#     data = (
#         work_orders_df.groupby("Sector")["Amount in Rupees (Excl of GST) (Masked)"]
#         .sum()
#         .reset_index()
#     )

#     fig = px.bar(
#         data,
#         x="Sector",
#         y="Amount in Rupees (Excl of GST) (Masked)",
#         title="Revenue by Sector",
#         color="Sector"
#     )

#     return fig


# # =========================
# # SMART GRAPH GENERATOR
# # =========================

# def generate_relevant_graphs(question, deals_df, work_orders_df):

#     q = question.lower()

#     graphs = []

#     # Sector related questions
#     if "sector" in q or "pipeline" in q:
#         graphs.append(pipeline_sector_chart(deals_df))

#     # Stage related questions
#     if "stage" in q or "progress" in q or "pipeline health" in q:
#         graphs.append(deals_stage_chart(deals_df))

#     # Probability questions
#     if "probability" in q or "close" in q or "conversion" in q:
#         graphs.append(deals_probability_chart(deals_df))

#     # Execution questions
#     if "execution" in q or "work order" in q or "delivery" in q:
#         graphs.append(execution_status_chart(work_orders_df))

#     # Revenue questions
#     if "revenue" in q or "performance" in q or "sector performing" in q:
#         revenue_chart = revenue_sector_chart(work_orders_df)
#         if revenue_chart:
#             graphs.append(revenue_chart)

#     # fallback: show core charts
#     if not graphs:
#         graphs = [
#             pipeline_sector_chart(deals_df),
#             deals_stage_chart(deals_df),
#             deals_probability_chart(deals_df)
#         ]

#     return graphs


# # =========================
# # TEST BLOCK
# # =========================

# if __name__ == "__main__":

#     deals_df = load_deals_dataframe()
#     work_orders_df = load_work_orders_dataframe()

#     question = "How healthy is our pipeline?"

#     print("\nTOTAL PIPELINE VALUE\n")
#     print(get_total_pipeline_value(deals_df))

#     print("\nPIPELINE BY SECTOR\n")
#     print(get_pipeline_by_sector(deals_df))

#     print("\nDEALS BY STAGE\n")
#     print(get_deals_by_stage(deals_df))

#     print("\nDEALS BY PROBABILITY\n")
#     print(get_deals_by_probability(deals_df))

#     print("\nWORK ORDER EXECUTION STATUS\n")
#     print(get_work_order_execution_status(work_orders_df))

#     print("\nREVENUE BY SECTOR\n")
#     print(get_revenue_by_sector(work_orders_df))

#     graphs = generate_relevant_graphs(question, deals_df, work_orders_df)

#     print(f"\nGenerated {len(graphs)} relevant graphs for the question.")


import pandas as pd
import plotly.express as px

from data_processor import load_deals_dataframe, load_work_orders_dataframe


# =========================
# BUSINESS INSIGHTS
# =========================

def get_total_pipeline_value(deals_df):
    return float(deals_df["Masked Deal value"].sum())


def get_pipeline_by_sector(deals_df):
    return (
        deals_df.groupby("Sector/service")["Masked Deal value"]
        .sum()
        .sort_values(ascending=False)
    )


def get_deals_by_stage(deals_df):
    return deals_df["Deal Stage"].value_counts()


def get_deals_by_probability(deals_df):
    return deals_df["Closure Probability"].value_counts()


def get_work_order_execution_status(work_orders_df):
    return work_orders_df["Execution Status"].value_counts()


def get_revenue_by_sector(work_orders_df):

    if "Amount in Rupees (Excl of GST) (Masked)" not in work_orders_df.columns:
        return None

    return (
        work_orders_df.groupby("Sector")["Amount in Rupees (Excl of GST) (Masked)"]
        .sum()
        .sort_values(ascending=False)
    )


# =========================
# GRAPH FUNCTIONS
# =========================

# PIPELINE BAR CHART
def pipeline_sector_bar(deals_df):

    data = (
        deals_df.groupby("Sector/service")["Masked Deal value"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        data,
        x="Sector/service",
        y="Masked Deal value",
        color="Sector/service",
        title="Pipeline Value by Sector"
    )

    return fig


# PIPELINE PIE CHART (same dataset as bar)
def pipeline_sector_pie(deals_df):

    data = (
        deals_df.groupby("Sector/service")["Masked Deal value"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        data,
        names="Sector/service",
        values="Masked Deal value",
        title="Pipeline Share by Sector"
    )

    return fig


# DEAL STAGE DISTRIBUTION
def deals_stage_horizontal(deals_df):

    data = deals_df["Deal Stage"].value_counts().reset_index()
    data.columns = ["Stage", "Count"]

    fig = px.bar(
        data,
        x="Count",
        y="Stage",
        orientation="h",
        color="Stage",
        title="Deal Stage Distribution"
    )

    return fig


# DEAL PROBABILITY DISTRIBUTION
def deals_probability_pie(deals_df):

    data = deals_df["Closure Probability"].value_counts().reset_index()
    data.columns = ["Probability", "Count"]

    fig = px.pie(
        data,
        names="Probability",
        values="Count",
        title="Deal Closure Probability Distribution"
    )

    return fig


# REVENUE DONUT CHART
def revenue_sector_donut(work_orders_df):

    if "Amount in Rupees (Excl of GST) (Masked)" not in work_orders_df.columns:
        return None

    data = (
        work_orders_df.groupby("Sector")["Amount in Rupees (Excl of GST) (Masked)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        data,
        names="Sector",
        values="Amount in Rupees (Excl of GST) (Masked)",
        hole=0.45,
        title="Revenue Share by Sector"
    )

    return fig


# REVENUE TREEMAP
def revenue_sector_treemap(work_orders_df):

    if "Amount in Rupees (Excl of GST) (Masked)" not in work_orders_df.columns:
        return None

    data = (
        work_orders_df.groupby("Sector")["Amount in Rupees (Excl of GST) (Masked)"]
        .sum()
        .reset_index()
    )

    fig = px.treemap(
        data,
        path=["Sector"],
        values="Amount in Rupees (Excl of GST) (Masked)",
        title="Revenue Contribution by Sector"
    )

    return fig

# =========================
# CHECKBOX GRAPH GENERATOR
# =========================

def generate_selected_graphs(selected_charts, deals_df, work_orders_df):

    graphs = []

    if "Bar Chart" in selected_charts:
        graphs.append(pipeline_sector_bar(deals_df))

    if "Pie Chart" in selected_charts:
        graphs.append(deals_probability_pie(deals_df))

    if "Donut Chart" in selected_charts:

        donut = revenue_sector_donut(work_orders_df)
        if donut:
            graphs.append(donut)

    if "Horizontal Bar" in selected_charts:
        graphs.append(deals_stage_horizontal(deals_df))

    if "Treemap" in selected_charts:

        treemap = revenue_sector_treemap(work_orders_df)
        if treemap:
            graphs.append(treemap)

    return graphs


# =========================
# TEST BLOCK
# =========================

if __name__ == "__main__":

    deals_df = load_deals_dataframe()
    work_orders_df = load_work_orders_dataframe()

    print("\nTOTAL PIPELINE VALUE\n")
    print(get_total_pipeline_value(deals_df))

    print("\nPIPELINE BY SECTOR\n")
    print(get_pipeline_by_sector(deals_df))

    print("\nDEALS BY STAGE\n")
    print(get_deals_by_stage(deals_df))

    print("\nDEALS BY PROBABILITY\n")
    print(get_deals_by_probability(deals_df))

    print("\nWORK ORDER EXECUTION STATUS\n")
    print(get_work_order_execution_status(work_orders_df))

    print("\nREVENUE BY SECTOR\n")
    print(get_revenue_by_sector(work_orders_df))

    charts = [
        "Bar Chart",
        "Pie Chart",
        "Donut Chart",
        "Horizontal Bar",
        "Treemap"
    ]

    graphs = generate_selected_graphs(charts, deals_df, work_orders_df)

    print(f"\nGenerated {len(graphs)} graphs.")