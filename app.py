import streamlit as st
from query_agent import analyze_business
from insights_engine import generate_selected_graphs
from report_generator import generate_report
from data_processor import load_deals_dataframe, load_work_orders_dataframe

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(page_title="Skylark AI", layout="wide")

# ---------------------------------
# DARK THEME CSS
# ---------------------------------

st.markdown("""
<style>

.stApp {
background-color:#0f172a;
color:white;
}

section[data-testid="stSidebar"]{
background-color:#020617;
}

h1,h2,h3,h4 {
color:white;
}

button{
border-radius:20px !important;
background:linear-gradient(90deg,#6366f1,#8b5cf6) !important;
color:white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# LOAD DATA
# ---------------------------------

deals_df = load_deals_dataframe()
work_orders_df = load_work_orders_dataframe()

# ---------------------------------
# SESSION STATE
# ---------------------------------

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# ---------------------------------
# SIDEBAR
# ---------------------------------

with st.sidebar:

    st.title("🚀 Skylark AI")

    if st.button("➕ New Chat"):

        chat_name = f"Chat {len(st.session_state.chats)+1}"

        st.session_state.chats[chat_name] = {
            "messages": [],
            "question": None,
            "insights": None
        }

        st.session_state.current_chat = chat_name

    st.divider()

    for chat in st.session_state.chats:

        if st.button(chat):
            st.session_state.current_chat = chat

# ---------------------------------
# IF NO CHAT
# ---------------------------------

if st.session_state.current_chat is None:
    st.markdown("## Start a new chat from the sidebar")
    st.stop()

chat = st.session_state.current_chat

# ---------------------------------
# CHAT WINDOW
# ---------------------------------

st.markdown("## 🤖 Skylark Business Intelligence Assistant")

messages = st.session_state.chats[chat]["messages"]

for msg in messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------------------------
# QUESTION INPUT
# ---------------------------------

question = st.chat_input("Ask a business question")

if question:

    st.session_state.chats[chat]["messages"].append(
        {"role":"user","content":question}
    )

    answer, insights = analyze_business(question)

    st.session_state.chats[chat]["messages"].append(
        {"role":"assistant","content":answer}
    )

    st.session_state.chats[chat]["question"] = question
    st.session_state.chats[chat]["insights"] = insights

    st.rerun()

# ---------------------------------
# GRAPH SECTION
# ---------------------------------

st.markdown("---")
st.markdown("## 📊 Visualisations")

current_question = st.session_state.chats[chat]["question"]
current_insights = st.session_state.chats[chat]["insights"]

if current_question is None:
    st.info("Ask a question first to generate visualisations.")

else:

    st.markdown(f"**Graphs for:** _{current_question}_")

    # Recommended charts from AI
    recommended = current_insights.get("recommended_charts", [])

    if recommended:
        st.markdown("### 🤖 AI Recommended Visualisations")
        for r in recommended:
            st.markdown(f"- {r}")

    selected_charts = []

    gcol1, gcol2, gcol3 = st.columns(3)

    with gcol1:
        bar = st.checkbox(
            "Bar Chart (Pipeline by Sector)",
            value="Bar Chart" in recommended,
            key=f"{chat}_bar"
        )
        if bar:
            selected_charts.append("Bar Chart")

        hbar = st.checkbox(
            "Horizontal Bar (Deal Stages)",
            value="Horizontal Bar" in recommended,
            key=f"{chat}_hbar"
        )
        if hbar:
            selected_charts.append("Horizontal Bar")

    with gcol2:
        pie = st.checkbox(
            "Pie Chart (Pipeline Share)",
            value="Pie Chart" in recommended,
            key=f"{chat}_pie"
        )
        if pie:
            selected_charts.append("Pie Chart")

        donut = st.checkbox(
            "Donut Chart (Revenue Share)",
            value="Donut Chart" in recommended,
            key=f"{chat}_donut"
        )
        if donut:
            selected_charts.append("Donut Chart")

    with gcol3:
        treemap = st.checkbox(
            "Treemap (Sector Revenue Contribution)",
            value="Treemap" in recommended,
            key=f"{chat}_treemap"
        )
        if treemap:
            selected_charts.append("Treemap")

    if st.button("Generate Graphs", key=f"{chat}_generate_graphs"):

        graphs = generate_selected_graphs(
            selected_charts,
            deals_df,
            work_orders_df
        )

        st.markdown("### Generated Visualisations")

        for fig in graphs:

            fig.update_layout(
                template="plotly_dark",
                height=450,
                margin=dict(l=10, r=10, t=40, b=10)
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displaylogo": False,
                    "toImageButtonOptions": {
                        "format": "png",
                        "filename": "skylark_graph",
                        "scale": 3
                    }
                }
            )

# ---------------------------------
# REPORT SECTION
# ---------------------------------

st.markdown("---")
st.markdown("## 📄 Generate Report")

if current_question is None:
    st.info("Ask a question first before generating a report.")

else:

    st.markdown(f"**Report for:** _{current_question}_")

    # AI suggested report sections
    recommended_sections = [
        "Executive Summary",
        "Pipeline Overview",
        "Key Insights",
        "Recommendations"
    ]

    st.markdown("### 🤖 AI Recommended Report Sections")
    for r in recommended_sections:
        st.markdown(f"- {r}")

    sections = []

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        r1 = st.checkbox(
            "Executive Summary",
            value="Executive Summary" in recommended_sections,
            key=f"{chat}_r1"
        )
        if r1:
            sections.append("Executive Summary")

    with col2:
        r2 = st.checkbox(
            "Key Insights",
            value="Key Insights" in recommended_sections,
            key=f"{chat}_r2"
        )
        if r2:
            sections.append("Key Insights")

    with col3:
        r3 = st.checkbox(
            "Pipeline Overview",
            value="Pipeline Overview" in recommended_sections,
            key=f"{chat}_r3"
        )
        if r3:
            sections.append("Pipeline Overview")

    with col4:
        r4 = st.checkbox(
            "Sector Performance",
            key=f"{chat}_r4"
        )
        if r4:
            sections.append("Sector Performance")

    col5,col6,col7,col8 = st.columns(4)

    with col5:
        r5 = st.checkbox("Deal Stage Analysis", key=f"{chat}_r5")
        if r5:
            sections.append("Deal Stage Analysis")

    with col6:
        r6 = st.checkbox("Visualisations", key=f"{chat}_r6")
        if r6:
            sections.append("Visualisations")

    with col7:
        r7 = st.checkbox("Statistical Data", key=f"{chat}_r7")
        if r7:
            sections.append("Statistical Data")

    with col8:
        r8 = st.checkbox(
            "Recommendations",
            value="Recommendations" in recommended_sections,
            key=f"{chat}_r8"
        )
        if r8:
            sections.append("Recommendations")

    if st.button("Generate Report", key=f"{chat}_generate_report"):

        report_file = generate_report(
            current_question,
            sections
        )

        with open(report_file,"rb") as file:

            st.download_button(
                label="⬇ Download Report",
                data=file,
                file_name=report_file
            )