import os
from groq import Groq
from dotenv import load_dotenv

from insights_engine import (
    get_total_pipeline_value,
    get_pipeline_by_sector,
    get_deals_by_stage,
    get_deals_by_probability,
    get_work_order_execution_status,
    get_revenue_by_sector
)

from data_processor import load_deals_dataframe, load_work_orders_dataframe


# -------------------------------------
# LOAD API
# -------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)


# -------------------------------------
# INTENT DETECTION
# -------------------------------------

def detect_intent(question):

    q = question.lower()

    if "pipeline" in q:
        return "pipeline_health"

    if "sector" in q:
        return "sector_analysis"

    if "stage" in q or "progress" in q:
        return "deal_stage"

    if "probability" in q or "risk" in q:
        return "deal_risk"

    if "revenue" in q or "performance" in q:
        return "revenue_analysis"

    return "general"


# -------------------------------------
# KPI CALCULATIONS
# -------------------------------------

def calculate_kpis(total_pipeline, pipeline_by_sector, deals_by_stage):

    kpis = {}

    if pipeline_by_sector:

        top_sector = max(pipeline_by_sector, key=pipeline_by_sector.get)

        share = pipeline_by_sector[top_sector] / total_pipeline if total_pipeline else 0

        kpis["top_sector"] = top_sector
        kpis["top_sector_share"] = round(share * 100, 2)

    if deals_by_stage:

        top_stage = max(deals_by_stage, key=deals_by_stage.get)

        kpis["largest_stage"] = top_stage
        kpis["largest_stage_count"] = deals_by_stage[top_stage]

    return kpis


# -------------------------------------
# RISK DETECTION
# -------------------------------------

def detect_risks(kpis):

    risks = []

    if "top_sector_share" in kpis:

        if kpis["top_sector_share"] > 60:
            risks.append("High pipeline concentration in a single sector")

    if "largest_stage" in kpis:

        if "Proposal" in kpis["largest_stage"]:
            risks.append("Large number of deals stuck in proposal stage")

    return risks


# -------------------------------------
# CHART RECOMMENDATION
# -------------------------------------

def recommend_charts(intent):

    if intent == "pipeline_health":
        return ["Bar Chart", "Pie Chart", "Horizontal Bar"]

    if intent == "sector_analysis":
        return ["Bar Chart", "Treemap"]

    if intent == "deal_stage":
        return ["Horizontal Bar"]

    if intent == "deal_risk":
        return ["Pie Chart"]

    if intent == "revenue_analysis":
        return ["Donut Chart", "Treemap"]

    return ["Bar Chart"]


# -------------------------------------
# MAIN ANALYSIS FUNCTION
# -------------------------------------

def analyze_business(question):

    deals_df = load_deals_dataframe()
    work_orders_df = load_work_orders_dataframe()

    # -------------------------
    # Metrics
    # -------------------------

    total_pipeline = get_total_pipeline_value(deals_df)

    pipeline_by_sector = get_pipeline_by_sector(deals_df)
    deals_by_stage = get_deals_by_stage(deals_df)
    deals_by_probability = get_deals_by_probability(deals_df)
    execution_status = get_work_order_execution_status(work_orders_df)

    revenue = get_revenue_by_sector(work_orders_df)
    revenue_by_sector = revenue if revenue is not None else {}

    # -------------------------
    # Intent
    # -------------------------

    intent = detect_intent(question)

    # -------------------------
    # KPIs
    # -------------------------

    kpis = calculate_kpis(
        total_pipeline,
        pipeline_by_sector.to_dict(),
        deals_by_stage.to_dict()
    )

    # -------------------------
    # Risks
    # -------------------------

    risks = detect_risks(kpis)

    # -------------------------
    # Chart Recommendations
    # -------------------------

    recommended_charts = recommend_charts(intent)

    # -------------------------
    # Insights Object
    # -------------------------

    insights = {
        "intent": intent,
        "total_pipeline": float(total_pipeline),
        "pipeline_by_sector": pipeline_by_sector.to_dict(),
        "deals_by_stage": deals_by_stage.to_dict(),
        "deals_by_probability": deals_by_probability.to_dict(),
        "execution_status": execution_status.to_dict(),
        "revenue_by_sector": revenue_by_sector.to_dict() if revenue is not None else {},
        "kpis": kpis,
        "risks": risks,
        "recommended_charts": recommended_charts
    }

    # -------------------------
    # LLM Prompt
    # -------------------------

    prompt = f"""
You are a senior business intelligence analyst preparing insights for leadership.

Use ONLY the provided business data.

BUSINESS DATA
{insights}

USER QUESTION
{question}

Provide:

1. Current situation
2. Important patterns
3. Risks or opportunities
4. Strategic observations leadership should know

Be concise and professional.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a senior business intelligence analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    return answer, insights


# -------------------------------------
# TEST MODE
# -------------------------------------

if __name__ == "__main__":

    question = input("Ask a business question: ")

    answer, insights = analyze_business(question)

    print("\nAI Insight:\n")
    print(answer)

    print("\nStructured Insights:\n")
    print(insights)