import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os
import subprocess
import plotly.graph_objects as go
import plotly.express as px
import warnings
import asyncio

# Windows asyncio fix for Python 3.14
warnings.filterwarnings("ignore", category=ResourceWarning)
if os.name == 'nt':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="RCA Bot Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# STYLING
# ==========================================
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATABASE CONNECTION
# ==========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "database", "rca.db")

@st.cache_resource
def get_connection():
    try:
        return sqlite3.connect(DB_FILE, check_same_thread=False)
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def query_database(query, params=()):
    """Execute database query"""
    try:
        conn = get_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except Exception as e:
        st.error(f"Query failed: {e}")
        return []

def get_column_names(query):
    """Get column names for query"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        return [description[0] for description in cursor.description]
    except:
        return []

def extract_confidence_score(report):
    """Extract confidence score from RCA report"""
    try:
        if "Confidence Score:" in report:
            score_text = report.split("Confidence Score:")[-1].strip()
            score = ''.join(filter(str.isdigit, score_text.split()[0]))
            return int(score) if score else 0
        return 0
    except:
        return 0

# ==========================================
# SIDEBAR - NAVIGATION
# ==========================================
st.sidebar.title("🤖 RCA Bot")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📈 History", "🔍 Search", "📉 Statistics", "🚀 Manual RCA"],
    index=0
)

st.sidebar.divider()
st.sidebar.subheader("About")
st.sidebar.info("""
**RCA Bot Dashboard** v1.0

Automated Root Cause Analysis for Pipeline Failures

- 🤖 AI-powered analysis
- 📊 Historical tracking
- 📢 Discord alerts
- 🎯 100% automation
""")

# ==========================================
# PAGE 1: DASHBOARD
# ==========================================
if page == "📊 Dashboard":
    st.title("🤖 RCA Bot Dashboard")
    st.write("Real-time Root Cause Analysis Intelligence")
    st.divider()
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    # Total Failures
    total = query_database("SELECT COUNT(*) FROM pipeline_failures")
    total_count = total[0][0] if total else 0
    col1.metric("📍 Total Failures", total_count)
    
    # This Week
    week = query_database("""
        SELECT COUNT(*) FROM pipeline_failures 
        WHERE datetime(timestamp) > datetime('now', '-7 days')
    """)
    week_count = week[0][0] if week else 0
    col2.metric("📅 This Week", week_count)
    
    # Today
    today = query_database("""
        SELECT COUNT(*) FROM pipeline_failures 
        WHERE datetime(timestamp) > datetime('now', '-1 day')
    """)
    today_count = today[0][0] if today else 0
    col3.metric("🕐 Today", today_count)
    
    # Average Confidence
    conf = query_database("""
        SELECT ROUND(AVG(CAST(SUBSTR(rca_report, INSTR(rca_report, 'Confidence Score: ') + 18, 3) AS INTEGER)))
        FROM pipeline_failures
        WHERE rca_report LIKE '%Confidence Score:%'
    """)
    avg_conf = conf[0][0] if conf and conf[0][0] else 0
    col4.metric("🎯 Avg Confidence", f"{avg_conf}%")
    
    st.divider()
    
    # Latest Failures
    st.subheader("📌 Latest RCA Reports")
    
    results = query_database("""
        SELECT id, timestamp, substr(rca_report, 1, 800) as report 
        FROM pipeline_failures 
        ORDER BY id DESC 
        LIMIT 5
    """)
    
    if results:
        for id, timestamp, report in results:
            confidence = extract_confidence_score(report)
            
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                
                with col1:
                    st.write(f"**ID:** `{id}`")
                    st.write(f"**Confidence:** {confidence}%")
                
                with col2:
                    st.write(f"**{timestamp}**")
                    st.write(report[:500] + "..." if len(report) > 500 else report)
                
                with col3:
                    if confidence >= 90:
                        st.markdown("🟢 **High**")
                    elif confidence >= 70:
                        st.markdown("🟡 **Medium**")
                    else:
                        st.markdown("🔴 **Low**")
                
                st.divider()
    else:
        st.info("📭 No failures recorded yet")

# ==========================================
# PAGE 2: HISTORY
# ==========================================
elif page == "📈 History":
    st.title("📈 Failure History")
    st.write("View and analyze failure records over time")
    st.divider()
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        days = st.number_input("Show last N days:", value=30, min_value=1, max_value=365)
    
    with col2:
        limit = st.number_input("Show last N records:", value=50, min_value=1, max_value=500)
    
    start_date = datetime.now() - timedelta(days=days)
    
    results = query_database("""
        SELECT id, timestamp, 
               substr(rca_report, 1, 200) as report_preview,
               CAST(SUBSTR(rca_report, INSTR(rca_report, 'Confidence Score: ') + 18, 3) AS INTEGER) as confidence
        FROM pipeline_failures 
        WHERE datetime(timestamp) > ?
        ORDER BY id DESC
        LIMIT ?
    """, (start_date.isoformat(), limit))
    
    if results:
        df = pd.DataFrame(results, columns=["ID", "Timestamp", "Report Preview", "Confidence"])
        
        # Style dataframe
        st.dataframe(
            df,
            use_container_width=True,
            height=500,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width=50),
                "Timestamp": st.column_config.TextColumn("Timestamp", width=200),
                "Report Preview": st.column_config.TextColumn("Report Preview", width=400),
                "Confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=100)
            }
        )
        
        st.success(f"✅ Found {len(df)} failures")
        
        # Download CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"rca_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("❌ No failures in selected period")

# ==========================================
# PAGE 3: SEARCH
# ==========================================
elif page == "🔍 Search":
    st.title("🔍 Search Failures")
    st.write("Find specific RCA reports by keyword")
    st.divider()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        keyword = st.text_input(
            "Search keyword:",
            placeholder="e.g., database, timeout, connection, permission, deploy...",
            key="search_keyword"
        )
    
    with col2:
        search_button = st.button("🔎 Search", use_container_width=True)
    
    if search_button and keyword:
        results = query_database("""
            SELECT id, timestamp, rca_report
            FROM pipeline_failures 
            WHERE rca_report LIKE ? 
            ORDER BY id DESC
        """, (f"%{keyword}%",))
        
        if results:
            st.success(f"✅ Found {len(results)} matching reports")
            st.divider()
            
            for id, timestamp, report in results:
                confidence = extract_confidence_score(report)
                
                with st.expander(f"📌 **{timestamp}** (ID: {id}, Confidence: {confidence}%)"):
                    st.write(report)
                    
                    # Copy button
                    st.button(
                        "📋 Copy Report",
                        key=f"copy_{id}",
                        on_click=lambda: st.write("Copied!")
                    )
        else:
            st.warning(f"❌ No results for keyword: '{keyword}'")
    
    elif keyword and not search_button:
        st.info("Click 'Search' to find matching reports")

# ==========================================
# PAGE 4: STATISTICS
# ==========================================
elif page == "📉 Statistics":
    st.title("📉 Statistics & Analytics")
    st.write("Trends, patterns, and insights from failure data")
    st.divider()
    
    # Key Metrics
    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    # Total
    total = query_database("SELECT COUNT(*) FROM pipeline_failures")
    col1.metric("Total Failures", total[0][0] if total else 0)
    
    # This Week
    week = query_database("""
        SELECT COUNT(*) FROM pipeline_failures 
        WHERE datetime(timestamp) > datetime('now', '-7 days')
    """)
    col2.metric("This Week", week[0][0] if week else 0)
    
    # This Month
    month = query_database("""
        SELECT COUNT(*) FROM pipeline_failures 
        WHERE datetime(timestamp) > datetime('now', '-30 days')
    """)
    col3.metric("This Month", month[0][0] if month else 0)
    
    # Average Confidence
    conf = query_database("""
        SELECT ROUND(AVG(CAST(SUBSTR(rca_report, INSTR(rca_report, 'Confidence Score: ') + 18, 3) AS INTEGER)))
        FROM pipeline_failures
        WHERE rca_report LIKE '%Confidence Score:%'
    """)
    col4.metric("Avg Confidence", f"{conf[0][0] if conf and conf[0][0] else 0}%")
    
    st.divider()
    
    # Failure Trend Chart
    st.subheader("📈 Failure Trend (Last 30 Days)")
    
    trend_data = query_database("""
        SELECT DATE(timestamp) as date, COUNT(*) as count
        FROM pipeline_failures
        WHERE datetime(timestamp) > datetime('now', '-30 days')
        GROUP BY DATE(timestamp)
        ORDER BY date
    """)
    
    if trend_data:
        df_trend = pd.DataFrame(trend_data, columns=["Date", "Failures"])
        
        fig = px.line(
            df_trend,
            x="Date",
            y="Failures",
            markers=True,
            title="Failure Trend",
            labels={"Failures": "Number of Failures", "Date": "Date"},
            template="plotly_dark"
        )
        fig.update_traces(line=dict(color="#667eea", width=3), marker=dict(size=8))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📭 No data to display")
    
    st.divider()
    
    # Confidence Distribution
    st.subheader("📊 Confidence Score Distribution")
    
    conf_data = query_database("""
        SELECT 
            CASE 
                WHEN CAST(SUBSTR(rca_report, INSTR(rca_report, 'Confidence Score: ') + 18, 3) AS INTEGER) >= 90 THEN 'High (90-100%)'
                WHEN CAST(SUBSTR(rca_report, INSTR(rca_report, 'Confidence Score: ') + 18, 3) AS INTEGER) >= 70 THEN 'Medium (70-89%)'
                ELSE 'Low (<70%)'
            END as category,
            COUNT(*) as count
        FROM pipeline_failures
        WHERE rca_report LIKE '%Confidence Score:%'
        GROUP BY category
    """)
    
    if conf_data:
        df_conf = pd.DataFrame(conf_data, columns=["Confidence Level", "Count"])
        
        fig_conf = px.pie(
            df_conf,
            names="Confidence Level",
            values="Count",
            title="Confidence Score Distribution",
            color_discrete_map={
                "High (90-100%)": "#2ecc71",
                "Medium (70-89%)": "#f39c12",
                "Low (<70%)": "#e74c3c"
            }
        )
        st.plotly_chart(fig_conf, use_container_width=True)

# ==========================================
# PAGE 5: MANUAL RCA
# ==========================================
elif page == "🚀 Manual RCA":
    st.title("🚀 Manual RCA Trigger")
    st.write("Run RCA analysis manually")
    st.divider()
    
    st.info("""
    Use this to manually trigger RCA analysis.
    Normally, RCA runs automatically when pipeline fails.
    """)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("▶️ Run RCA Now", use_container_width=True):
            with st.spinner("⏳ Running RCA Agent..."):
                try:
                    # Run RCA agent
                    result = subprocess.run(
                        ["python", os.path.join(BASE_DIR, "RCA_bot", "rca_agent.py")],
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    
                    if result.returncode == 0:
                        st.success("✅ RCA completed successfully!")
                        
                        # Show output
                        with st.expander("📝 Agent Output"):
                            st.code(result.stdout)
                        
                        # Try to send alert
                        with st.spinner("📢 Sending Discord alert..."):
                            alert_result = subprocess.run(
                                ["python", os.path.join(BASE_DIR, "RCA_bot", "send_discord_alert.py")],
                                capture_output=True,
                                text=True,
                                timeout=30
                            )
                            
                            if alert_result.returncode == 0:
                                st.success("✅ Discord alert sent!")
                            else:
                                st.warning(f"⚠️ Alert send failed: {alert_result.stderr}")
                    else:
                        st.error(f"❌ RCA failed: {result.stderr}")
                
                except subprocess.TimeoutExpired:
                    st.error("❌ RCA timed out after 5 minutes")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.write("""
        **What happens when you click 'Run RCA Now':**
        
        1. ✅ RCA Agent analyzes latest logs
        2. ✅ Generates Root Cause Analysis
        3. ✅ Saves to database
        4. ✅ Sends Discord alert
        5. ✅ Displays results here
        
        **Typically takes 1-2 minutes**
        """)
    
    st.divider()
    
    # Last RCA Report
    st.subheader("📄 Latest Report")
    
    latest = query_database("""
        SELECT timestamp, rca_report 
        FROM pipeline_failures 
        ORDER BY id DESC 
        LIMIT 1
    """)
    
    if latest:
        timestamp, report = latest[0]
        st.write(f"**Generated:** {timestamp}")
        st.write(report)
    else:
        st.info("📭 No reports generated yet")

# ==========================================
# FOOTER
# ==========================================
st.divider()
st.caption("""
🤖 **RCA Bot Dashboard v1.0** | Automated Root Cause Analysis
Built with Streamlit | Data stored in SQLite | Alerts via Discord
""")
