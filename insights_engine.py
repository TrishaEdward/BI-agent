import pandas as pd
import plotly.express as px

from data_processor import load_deals_dataframe, load_work_orders_dataframe


# =========================
# HELPER FUNCTION
# =========================

def find_column(df, keywords):
    """Find first column containing keyword"""
    for col in df.columns:
        for key in keywords:
            if key.lower() in col.lower():
                return col
    return None


# =========================
# BUSINESS INSIGHTS
# =========================

def get_total_pipeline_value(deals_df):

    value_col = find_column(deals_df, ["value"])

    if value_col is None:
        return 0

    return float(deals_df[value_col].fillna(0).sum())


def get_pipeline_by_sector(deals_df):

    value_col = find_column(deals_df, ["value"])
    sector_col = find_column(deals_df, ["sector"])

    if value_col is None or sector_col is None:
        return pd.Series(dtype=float)

    return (
        deals_df.groupby(sector_col)[value_col]
        .sum()
        .sort_values(ascending=False)
    )


def get_deals_by_stage(deals_df):

    stage_col = find_column(deals_df, ["stage"])

    if stage_col is None:
        return pd.Series(dtype=int)

    return deals_df[stage_col].value_counts()


def get_deals_by_probability(deals_df):

    prob_col = find_column(deals_df, ["probability"])

    if prob_col is None:
        return pd.Series(dtype=int)

    return deals_df[prob_col].value_counts()


def get_work_order_execution_status(work_orders_df):

    status_col = find_column(work_orders_df, ["execution", "status"])

    if status_col is None:
        return pd.Series(dtype=int)

    return work_orders_df[status_col].value_counts()


def get_revenue_by_sector(work_orders_df):

    revenue_col = find_column(work_orders_df, ["amount", "revenue"])
    sector_col = find_column(work_orders_df, ["sector"])

    if revenue_col is None or sector_col is None:
        return pd.Series(dtype=float)

    return (
        work_orders_df.groupby(sector_col)[revenue_col]
        .sum()
        .sort_values(ascending=False)
    )


# =========================
# GRAPH FUNCTIONS
# =========================

def pipeline_sector_bar(deals_df):

    value_col = find_column(deals_df, ["value"])
    sector_col = find_column(deals_df, ["sector"])

    if value_col is None or sector_col is None:
        return None

    data = (
        deals_df.groupby(sector_col)[value_col]
        .sum()
        .reset_index()
    )

    return px.bar(
        data,
        x=sector_col,
        y=value_col,
        color=sector_col,
        title="Pipeline Value by Sector"
    )


def pipeline_sector_pie(deals_df):

    value_col = find_column(deals_df, ["value"])
    sector_col = find_column(deals_df, ["sector"])

    if value_col is None or sector_col is None:
        return None

    data = (
        deals_df.groupby(sector_col)[value_col]
        .sum()
        .reset_index()
    )

    return px.pie(
        data,
        names=sector_col,
        values=value_col,
        title="Pipeline Share by Sector"
    )


def deals_stage_horizontal(deals_df):

    stage_col = find_column(deals_df, ["stage"])

    if stage_col is None:
        return None

    data = deals_df[stage_col].value_counts().reset_index()
    data.columns = ["Stage", "Count"]

    return px.bar(
        data,
        x="Count",
        y="Stage",
        orientation="h",
        color="Stage",
        title="Deal Stage Distribution"
    )


def deals_probability_pie(deals_df):

    prob_col = find_column(deals_df, ["probability"])

    if prob_col is None:
        return None

    data = deals_df[prob_col].value_counts().reset_index()
    data.columns = ["Probability", "Count"]

    return px.pie(
        data,
        names="Probability",
        values="Count",
        title="Deal Closure Probability Distribution"
    )


def revenue_sector_donut(work_orders_df):

    revenue_col = find_column(work_orders_df, ["amount", "revenue"])
    sector_col = find_column(work_orders_df, ["sector"])

    if revenue_col is None or sector_col is None:
        return None

    data = (
        work_orders_df.groupby(sector_col)[revenue_col]
        .sum()
        .reset_index()
    )

    return px.pie(
        data,
        names=sector_col,
        values=revenue_col,
        hole=0.45,
        title="Revenue Share by Sector"
    )


def revenue_sector_treemap(work_orders_df):

    revenue_col = find_column(work_orders_df, ["amount", "revenue"])
    sector_col = find_column(work_orders_df, ["sector"])

    if revenue_col is None or sector_col is None:
        return None

    data = (
        work_orders_df.groupby(sector_col)[revenue_col]
        .sum()
        .reset_index()
    )

    return px.treemap(
        data,
        path=[sector_col],
        values=revenue_col,
        title="Revenue Contribution by Sector"
    )


# =========================
# GRAPH GENERATOR
# =========================

def generate_selected_graphs(selected_charts, deals_df, work_orders_df):

    graphs = []

    if "Bar Chart" in selected_charts:
        g = pipeline_sector_bar(deals_df)
        if g:
            graphs.append(g)

    if "Pie Chart" in selected_charts:
        g = pipeline_sector_pie(deals_df)
        if g:
            graphs.append(g)

    if "Donut Chart" in selected_charts:
        g = revenue_sector_donut(work_orders_df)
        if g:
            graphs.append(g)

    if "Horizontal Bar" in selected_charts:
        g = deals_stage_horizontal(deals_df)
        if g:
            graphs.append(g)

    if "Treemap" in selected_charts:
        g = revenue_sector_treemap(work_orders_df)
        if g:
            graphs.append(g)

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