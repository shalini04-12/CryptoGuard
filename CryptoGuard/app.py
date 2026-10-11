import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from src.inventory import load_inventory, analyze_inventory


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="CryptoGuard | Quantum Security",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# DARK CYBER THEME
# Keep this as one complete string. Do not add Markdown
# code fences around the CSS.
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at 10% 0%, rgba(0,229,255,.08), transparent 35%),
            radial-gradient(ellipse at 95% 10%, rgba(139,92,246,.10), transparent 32%),
            #080B16;
        color: #E8EEFF;
    }
    .block-container {max-width: 1500px; padding-top: 2rem; padding-bottom: 3rem;}
    h1, h2, h3 {color: #F3F6FF !important; letter-spacing: -.3px;}
    .stMarkdown p, .stMarkdown li {color: #B8C3DC; line-height: 1.65;}
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #151D31, #0D1323);
        border: 1px solid rgba(115,135,180,.28);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 28px rgba(0,0,0,.18);
    }
    [data-testid="stMetricLabel"] {color: #AAB7D1 !important;}
    [data-testid="stMetricValue"] {color: #00E5FF !important; font-weight: 750;}
    [data-testid="stSidebar"] {
        background: #0D1221;
        border-right: 1px solid rgba(139,92,246,.25);
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {color: #00E5FF !important;}
    .stButton button, .stDownloadButton button {
        background: linear-gradient(100deg, #087FAD, #6552D9);
        color: white;
        border: 1px solid rgba(0,229,255,.35);
        border-radius: 10px;
        font-weight: 650;
    }
    .stButton button:hover, .stDownloadButton button:hover {
        border-color: #00E5FF;
        color: white;
        box-shadow: 0 0 16px rgba(0,229,255,.2);
    }
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(115,135,180,.25);
        border-radius: 12px;
    }
    [data-testid="stExpander"] {
        background: rgba(17,24,39,.75);
        border: 1px solid rgba(115,135,180,.25);
        border-radius: 12px;
        margin-bottom: 8px;
    }
    [data-testid="stFileUploader"] {
        background: rgba(17,24,39,.55);
        border: 1px dashed rgba(0,229,255,.35);
        border-radius: 12px;
        padding: 10px;
    }
    [data-testid="stAlert"] {border-radius: 12px;}
    hr {border-color: rgba(115,135,180,.22);}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# PDF REPORT
# ---------------------------------------------------------
def generate_pdf_report(results):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CGReportTitle",
        parent=styles["Title"],
        fontSize=22,
        leading=27,
        textColor=colors.HexColor("#087FAD"),
        alignment=TA_CENTER,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="CGSmallCell",
        parent=styles["BodyText"],
        fontSize=7,
        leading=9,
        wordWrap="CJK",
    ))

    story = [
        Paragraph("CryptoGuard", styles["CGReportTitle"]),
        Paragraph(
            "Cryptographic Intelligence &amp; Migration Framework",
            styles["Heading2"],
        ),
        Spacer(1, 4 * mm),
        Paragraph(
            "Preliminary cryptographic inventory and quantum-risk assessment",
            styles["Normal"],
        ),
        Spacer(1, 5 * mm),
    ]

    total_assets = len(results)
    high_risk = int((results["quantum_risk"] == "High").sum())
    unknown_assets = int((results["quantum_risk"] == "Unknown").sum())
    average_score = round(results["risk_score"].mean(), 1) if total_assets else 0

    summary = [
        ["Total Assets", "High-Risk Assets", "Unknown Algorithms", "Average Risk Score"],
        [str(total_assets), str(high_risk), str(unknown_assets), f"{average_score}/100"],
    ]
    summary_table = Table(summary, colWidths=[60 * mm] * 4)
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172554")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#EAF2FF")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [summary_table, Spacer(1, 7 * mm)]
    story.append(Paragraph("Cryptographic Asset Inventory", styles["Heading1"]))
    story.append(Spacer(1, 3 * mm))

    columns = [
        "asset_id", "asset_name", "algorithm", "data_sensitivity",
        "exposure", "quantum_risk", "risk_score",
    ]
    headers = [
        "Asset ID", "Asset Name", "Algorithm", "Sensitivity",
        "Exposure", "Risk Category", "Score",
    ]
    table_data = [[Paragraph(escape(x), styles["CGSmallCell"]) for x in headers]]
    for _, row in results.iterrows():
        table_data.append([
            Paragraph(escape(str(row.get(col, ""))), styles["CGSmallCell"])
            for col in columns
        ])

    asset_table = Table(
        table_data,
        colWidths=[22 * mm, 48 * mm, 30 * mm, 28 * mm, 35 * mm, 32 * mm, 18 * mm],
        repeatRows=1,
    )
    asset_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172554")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FF")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [asset_table, Spacer(1, 7 * mm)]
    story.append(Paragraph("Migration Recommendations", styles["Heading1"]))

    for _, row in results.iterrows():
        asset_id = escape(str(row.get("asset_id", "")))
        asset_name = escape(str(row.get("asset_name", "")))
        algorithm = escape(str(row.get("algorithm", "")))
        risk = escape(str(row.get("quantum_risk", "")))
        score = escape(str(row.get("risk_score", "")))
        reason_value = row.get("risk_reason", "No additional risk explanation available.")
        options_value = row.get("migration_options", "Review the algorithm and plan migration.")
        reason = "No additional risk explanation available." if pd.isna(reason_value) else escape(str(reason_value))
        options = "Review the algorithm and plan migration." if pd.isna(options_value) else escape(str(options_value))

        story.append(Paragraph(f"<b>{asset_id} — {asset_name}</b>", styles["Heading3"]))
        story.append(Paragraph(
            f"<b>Algorithm:</b> {algorithm} &nbsp; | &nbsp; <b>Risk:</b> {risk} &nbsp; | &nbsp; <b>Score:</b> {score}/100",
            styles["Normal"],
        ))
        story.append(Paragraph(f"<b>Reason:</b> {reason}", styles["Normal"]))
        story.append(Paragraph(f"<b>Potential options:</b> {options}", styles["Normal"]))
        story.append(Spacer(1, 3 * mm))

    story += [
        Spacer(1, 4 * mm),
        Paragraph(
            "<b>Disclaimer:</b> CryptoGuard is a prototype. Scores are illustrative "
            "triage estimates, not official NIST or hackathon scoring formulas. "
            "Validate algorithms, implementations, and migration decisions with "
            "qualified security professionals.",
            styles["Italic"],
        ),
    ]

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


# ---------------------------------------------------------
# HEADER (native Streamlit text; no custom HTML)
# ---------------------------------------------------------
st.markdown("### ◈ QUANTUM SECURITY PLATFORM")
st.title("CryptoGuard")
st.subheader("Cryptographic Intelligence & Migration Framework")
st.write("Discover cryptographic risks. Prioritize vulnerabilities. Prepare for the quantum era.")
st.divider()


# ---------------------------------------------------------
# SIDEBAR / CSV UPLOAD
# ---------------------------------------------------------
st.sidebar.title("◈ CryptoGuard")
st.sidebar.caption("Cryptographic Intelligence")
st.sidebar.markdown("---")
st.sidebar.header("📂 Asset Inventory")
uploaded_file = st.sidebar.file_uploader(
    "Upload a cryptographic inventory CSV",
    type=["csv"],
)
st.sidebar.caption(
    "Required columns: asset_id, asset_name, algorithm, data_sensitivity, exposure"
)


# ---------------------------------------------------------
# LOAD INVENTORY
# ---------------------------------------------------------
if uploaded_file is None:
    st.info("Showing the sample inventory. Upload a CSV file in the sidebar to analyze your own assets.")
    try:
        inventory = load_inventory("data/raw/crypto_inventory.csv")
    except Exception as error:
        st.error(f"Could not load the sample inventory: {error}")
        st.stop()
else:
    try:
        inventory = load_inventory(uploaded_file)
    except Exception as error:
        st.error(f"Could not read the uploaded inventory: {error}")
        st.stop()

results = analyze_inventory(inventory)
if results.empty:
    st.warning("No assets are available to display.")
    st.stop()

st.info(
    "Prototype notice: Risk scores are illustrative estimates, "
    "not official NIST or hackathon scoring formulas."
)


# ---------------------------------------------------------
# SUMMARY METRICS
# ---------------------------------------------------------
total_assets = len(results)
high_risk = int((results["quantum_risk"] == "High").sum())
unknown_assets = int((results["quantum_risk"] == "Unknown").sum())
average_score = round(results["risk_score"].mean(), 1)

st.header("◈ Security Overview")
st.caption("A consolidated view of your cryptographic inventory and preliminary quantum-risk assessment.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("◈ Total Assets", total_assets)
c2.metric("⚠ High-Risk Assets", high_risk)
c3.metric("? Unknown Algorithms", unknown_assets)
c4.metric("◉ Average Risk Score", f"{average_score}/100")
st.divider()


# ---------------------------------------------------------
# CHARTS
# ---------------------------------------------------------
st.header("📊 Cryptographic Risk Intelligence")
st.caption("Compare preliminary risk scores and categories for the analyzed assets.")
chart_col1, chart_col2 = st.columns([1.5, 1])

with chart_col1:
    st.subheader("Risk Score by Asset")
    fig, ax = plt.subplots(figsize=(9, 4.3))
    fig.patch.set_facecolor("#0D1221")
    ax.set_facecolor("#0D1221")
    asset_ids = results["asset_id"].astype(str)
    scores = results["risk_score"]
    bars = ax.bar(asset_ids, scores, color="#00CFE8", edgecolor="#8B5CF6", linewidth=0.7)
    ax.set_ylim(0, 110)
    ax.set_xlabel("Asset ID", color="#B8C3DC")
    ax.set_ylabel("Risk Score", color="#B8C3DC")
    ax.tick_params(axis="x", colors="#B8C3DC", rotation=35)
    ax.tick_params(axis="y", colors="#B8C3DC")
    ax.grid(axis="y", linestyle="--", alpha=0.18, color="#8E9BB8")
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color("#28334B")
    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(score),
                ha="center", va="bottom", color="#E8EEFF", fontsize=8)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with chart_col2:
    st.subheader("Risk Distribution")
    risk_counts = results["quantum_risk"].value_counts()
    palette = {
        "High": "#FF4D6D", "Moderate": "#FBBF24", "Review": "#A78BFA",
        "PQC": "#00E5FF", "Unknown": "#94A3B8",
    }
    bar_colors = [palette.get(str(category), "#8B5CF6") for category in risk_counts.index]
    fig2, ax2 = plt.subplots(figsize=(6.5, 4.3))
    fig2.patch.set_facecolor("#0D1221")
    ax2.set_facecolor("#0D1221")
    bars2 = ax2.bar(risk_counts.index.astype(str), risk_counts.values, color=bar_colors)
    ax2.set_xlabel("Risk Category", color="#B8C3DC")
    ax2.set_ylabel("Number of Assets", color="#B8C3DC")
    ax2.tick_params(axis="x", colors="#B8C3DC", rotation=25)
    ax2.tick_params(axis="y", colors="#B8C3DC")
    ax2.grid(axis="y", linestyle="--", alpha=0.18, color="#8E9BB8")
    ax2.set_axisbelow(True)
    for spine in ax2.spines.values():
        spine.set_color("#28334B")
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height + 0.05, str(int(height)),
                 ha="center", va="bottom", color="#E8EEFF", fontsize=9)
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

st.divider()


# ---------------------------------------------------------
# INVENTORY TABLE + SEARCH
# ---------------------------------------------------------
st.header("🔐 Cryptographic Asset Inventory")
st.caption("Search and review algorithms, sensitivity, exposure, risk classification, and scores.")
search_query = st.text_input(
    "🔎 Search assets",
    placeholder="Search by asset ID, name, algorithm, or risk category...",
)
display_results = results.copy()
if search_query.strip():
    query = search_query.strip().lower()
    searchable = ["asset_id", "asset_name", "algorithm", "quantum_risk"]
    mask = pd.Series(False, index=display_results.index)
    for column in searchable:
        if column in display_results.columns:
            mask |= display_results[column].astype(str).str.lower().str.contains(query, na=False)
    display_results = display_results[mask]

st.dataframe(display_results, use_container_width=True, hide_index=True)
st.caption(f"Showing {len(display_results)} of {total_assets} assets.")
st.divider()


# ---------------------------------------------------------
# MIGRATION INTELLIGENCE
# ---------------------------------------------------------
st.header("🔄 Migration Intelligence")
st.caption("Review the preliminary risk assessment and suggested options for each asset.")

risk_colors = {
    "High": "#FF4D6D", "Moderate": "#FBBF24", "Review": "#A78BFA",
    "PQC": "#00E5FF", "Unknown": "#94A3B8",
}
for _, row in results.iterrows():
    asset_id = str(row["asset_id"])
    asset_name = str(row["asset_name"])
    risk = str(row["quantum_risk"])
    score = row["risk_score"]
    with st.expander(f"{asset_id} — {asset_name} | Risk: {risk} | Score: {score}/100"):
        left, right = st.columns(2)
        with left:
            st.write("**Current algorithm**")
            st.write(str(row["algorithm"]))
            st.write("**Data sensitivity**")
            st.write(str(row["data_sensitivity"]))
        with right:
            st.write("**Risk category**")
            st.markdown(f":red[{risk}]" if risk == "High" else f"**{risk}**")
            st.write("**Risk score**")
            st.write(f"{score}/100")
            st.write("**Exposure**")
            st.write(str(row["exposure"]))
        st.markdown("---")
        st.write("**Risk explanation**")
        st.write(str(row.get("risk_reason", "No additional explanation available.")))
        st.write("**Potential migration options**")
        st.write(str(row.get("migration_options", "Review the algorithm and plan migration.")))

st.divider()


# ---------------------------------------------------------
# REPORT CENTER
# ---------------------------------------------------------
st.header("📥 Report Center")
st.caption("Export the current assessment for documentation and review.")
download_col1, download_col2 = st.columns(2)

with download_col1:
    csv_data = results.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📊 Download Risk Assessment CSV",
        data=csv_data,
        file_name="cryptoguard_risk_assessment.csv",
        mime="text/csv",
        use_container_width=True,
    )

with download_col2:
    pdf_data = generate_pdf_report(results)
    st.download_button(
        "📄 Download Risk Assessment PDF",
        data=pdf_data,
        file_name="cryptoguard_risk_assessment.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

st.divider()
st.caption("◈ CRYPTOGUARD  |  Cryptographic Intelligence & Migration Framework")
st.caption("Prototype for preliminary quantum-risk assessment and cryptographic migration planning.")
