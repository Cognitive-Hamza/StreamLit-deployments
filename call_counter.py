import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Call Log Dashboard", layout="wide")

# =========================
# GLOBAL CSS FOR CENTERING TABLES
# =========================
st.markdown("""
<style>
table th, table td {
    text-align: center !important;
    vertical-align: middle !important;
}
.stButton > button {
    width: 100%;
    border-radius: 8px;
    height: 50px;
    font-size: 16px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE INITIALIZATION
# =========================
if 'page' not in st.session_state:
    st.session_state.page = 'upload'

# =========================
# FILE UPLOAD PAGE
# =========================
if st.session_state.page == 'upload':
    st.title("📞 Call Log Analysis Dashboard")
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])
    
    if uploaded_file is None:
        st.info("👆 Upload Excel file to start dashboard")
        
        sample_df = pd.DataFrame({
            "Call Date time": [
                "2025-12-01 09:05:39",
                "2025-12-01 09:11:41",
                "2025-12-01 10:36:31",
                "2025-12-01 11:32:17"
            ],
            "From": [
                "phn no.",
                "phn no.",
                "phn no.",
                "phn no."
            ],
            "To": [
                "phn no.",
                "phn no.",
                "phn no.",
                "phn no."
            ],
            "Duration": ["00:04:07", "00:03:26", "00:06:28", "00:03:44"],
            "Bill Sec": ["00:00:25", "00:03:26", "00:04:49", "00:03:33"],
            "Call Status": ["ANSWERED", "NO ANSWER", "ANSWERED", "ANSWERED"],
            "Call Type": ["inbound", "inbound", "inbound", "outbound"],
            "Agent Name": ["Name 1", "Name 2", "Name 3", "Name 4"],
            "Department": ["Sales", "Unknown", "Sales", "Sales"]
        })
        
        st.subheader("📋 Sample Excel Format")
        st.markdown(sample_df.to_html(index=False), unsafe_allow_html=True)
        st.stop()
    
    # Load and process data
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()
    
    required_cols = [
        "Call Date time", "Call Status",
        "Call Type", "Agent Name", "Duration", "Department"
    ]
    
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Missing columns: {', '.join(missing)}")
        st.stop()
    
    # Clean data
    df["Call Date time"] = pd.to_datetime(df["Call Date time"], errors="coerce")
    df = df.dropna(subset=["Call Date time"])
    df["hour"] = df["Call Date time"].dt.hour
    
    df["Call Type"] = df["Call Type"].str.lower().str.strip()
    df["Call Status"] = df["Call Status"].str.upper().str.strip()
    df["Agent Name"] = df["Agent Name"].str.strip()
    df["Department"] = df["Department"].str.strip()
    
    def duration_to_seconds(x):
        try:
            h, m, s = map(int, str(x).split(":"))
            return h*3600 + m*60 + s
        except:
            return 0
    
    df["duration_minutes"] = df["Duration"].apply(duration_to_seconds) / 60
    
    def duration_bucket(m):
        if m <= 0.5: return "0-30 sec"
        if m <= 1: return "30 sec-1 min"
        if m <= 2: return "1-2 min"
        if m <= 5: return "3-5 min"
        if m <= 10: return "5-10 min"
        if m <= 20: return "10-20 min"
        if m <= 30: return "20-30 min"
        return "30+ min"
    
    df["duration_category"] = df["duration_minutes"].apply(duration_bucket)
    
    # Store in session state
    st.session_state.df = df
    st.session_state.page = 'overview'
    st.rerun()

# =========================
# HELPER FUNCTION
# =========================
def build_agent_table(data):
    rows = []
    for agent in data["Agent Name"].unique():
        a = data[data["Agent Name"] == agent]
        
        dept = a["Department"].mode()[0] if len(a["Department"].mode()) > 0 else "Unknown"
        
        total_calls = len(a)
        
        # Calculate total duration in hours and minutes
        total_duration_mins = a["duration_minutes"].sum()
        total_hours = int(total_duration_mins // 60)
        total_mins = int(total_duration_mins % 60)
        
        rows.append({
            "Agent": agent,
            "Department": dept,
            "Total Calls": total_calls,
            "Total Duration": f"{total_hours}h {total_mins}m",
            "Sort_Minutes": total_duration_mins
        })
    
    df_out = pd.DataFrame(rows).sort_values("Sort_Minutes", ascending=False).reset_index(drop=True)
    df_out = df_out.drop(columns=["Sort_Minutes"])
    df_out.insert(0, "Rank", range(1, len(df_out)+1))
    return df_out

# =========================
# NAVIGATION
# =========================
if st.session_state.page != 'upload':
    df = st.session_state.df
    
    st.title("📞 Call Log Analysis Dashboard")
    
    # Navigation buttons
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        if st.button("📊 Overview"):
            st.session_state.page = 'overview'
            st.rerun()
    
    with col2:
        if st.button("📅 Peak Times"):
            st.session_state.page = 'peak'
            st.rerun()
    
    with col3:
        if st.button("🏆 Performance"):
            st.session_state.page = 'performance'
            st.rerun()
    
    with col4:
        if st.button("📥📤 Rankings"):
            st.session_state.page = 'rankings'
            st.rerun()
    
    with col5:
        if st.button("⏱️ Duration"):
            st.session_state.page = 'duration'
            st.rerun()
    
    with col6:
        if st.button("📝 Summary"):
            st.session_state.page = 'summary'
            st.rerun()
    
    with col7:
        if st.button("💾 Export"):
            st.session_state.page = 'export'
            st.rerun()
    
    st.markdown("---")

# =========================
# PAGE 1: OVERVIEW
# =========================
if st.session_state.page == 'overview':
    st.header("📊 Overview")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Calls", len(df))
    c2.metric("Total Agents", df["Agent Name"].nunique())
    
    answered = df[df["Call Status"] == "ANSWERED"]
    c3.metric("Answered Rate", f"{(len(answered)/len(df))*100:.1f}%")
    c4.metric("Not Answered", len(df[df["Call Status"] == "NO ANSWER"]))
    
    st.markdown("---")
    
    # Inbound vs Outbound Comparison
    st.subheader("📞 Inbound vs Outbound Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Call counts comparison
        inbound_count = len(df[df["Call Type"] == "inbound"])
        outbound_count = len(df[df["Call Type"] == "outbound"])
        
        fig = px.bar(
            x=["Inbound", "Outbound"],
            y=[inbound_count, outbound_count],
            title="Total Calls: Inbound vs Outbound",
            labels={"x": "Call Type", "y": "Number of Calls"},
            text=[inbound_count, outbound_count],
            color=["Inbound", "Outbound"],
            color_discrete_map={"Inbound": "#636EFA", "Outbound": "#EF553B"}
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Answer rate comparison
        inbound_df = df[df["Call Type"] == "inbound"]
        outbound_df = df[df["Call Type"] == "outbound"]
        
        inbound_answered = len(inbound_df[inbound_df["Call Status"] == "ANSWERED"])
        outbound_answered = len(outbound_df[outbound_df["Call Status"] == "ANSWERED"])
        
        inbound_rate = (inbound_answered / len(inbound_df) * 100) if len(inbound_df) else 0
        outbound_rate = (outbound_answered / len(outbound_df) * 100) if len(outbound_df) else 0
        
        fig = px.bar(
            x=["Inbound", "Outbound"],
            y=[inbound_rate, outbound_rate],
            title="Answer Rate: Inbound vs Outbound",
            labels={"x": "Call Type", "y": "Answer Rate (%)"},
            text=[f"{inbound_rate:.1f}%", f"{outbound_rate:.1f}%"],
            color=["Inbound", "Outbound"],
            color_discrete_map={"Inbound": "#00CC96", "Outbound": "#FFA15A"}
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed comparison table
    comparison_data = pd.DataFrame({
        "Metric": ["Total Calls", "Answered", "Not Answered", "Answer Rate"],
        "Inbound": [
            inbound_count,
            inbound_answered,
            len(inbound_df[inbound_df["Call Status"] == "NO ANSWER"]),
            f"{inbound_rate:.1f}%"
        ],
        "Outbound": [
            outbound_count,
            outbound_answered,
            len(outbound_df[outbound_df["Call Status"] == "NO ANSWER"]),
            f"{outbound_rate:.1f}%"
        ]
    })
    st.markdown(comparison_data.to_html(index=False), unsafe_allow_html=True)

# =========================
# PAGE 2: PEAK TIMES
# =========================
elif st.session_state.page == 'peak':
    st.header("📅 Peak Times Analysis")
    
    # Add day of week and day name
    df['day_of_week'] = df['Call Date time'].dt.dayofweek
    df['day_name'] = df['Call Date time'].dt.day_name()
    
    # Calls by Day of Week
    st.subheader("📊 Calls by Day of Week")
    
    day_counts = df.groupby(['day_of_week', 'day_name']).size().reset_index(name='count')
    day_counts = day_counts.sort_values('day_of_week')
    
    fig = px.bar(
        day_counts,
        x='day_name',
        y='count',
        title="Total Calls per Day of Week",
        labels={'day_name': 'Day of Week', 'count': 'Number of Calls'},
        text='count',
        color='count',
        color_continuous_scale='Blues'
    )
    fig.update_traces(textposition='outside')
    fig.update_xaxes(categoryorder='array', categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    st.plotly_chart(fig, use_container_width=True)
    
    # Table with day-wise breakdown
    day_table = pd.DataFrame({
        'Day': day_counts['day_name'],
        'Total Calls': day_counts['count'],
        'Percentage': (day_counts['count'] / day_counts['count'].sum() * 100).round(1).astype(str) + '%'
    })
    st.markdown(day_table.to_html(index=False), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Hourly Analysis
    st.subheader("⏰ Calls by Hour of Day")
    
    c1, c2 = st.columns(2)
    for call_type, col in zip(["inbound", "outbound"], [c1, c2]):
        subset = df[df["Call Type"] == call_type]
        if len(subset):
            hourly = subset.groupby("hour").size().reset_index(name="count")
            fig = px.line(hourly, x="hour", y="count", markers=True,
                         title=f"{call_type.title()} Calls by Hour")
            fig.update_xaxes(title="Hour of Day")
            fig.update_yaxes(title="Number of Calls")
            col.plotly_chart(fig, use_container_width=True)
    


# =========================
# PAGE 3: PERFORMANCE
# =========================
elif st.session_state.page == 'performance':
    st.header("👥 Overall Agent Performance")
    overall_table = build_agent_table(df)
    st.markdown(overall_table.to_html(index=False), unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.header("🏆 Agent Leaderboard")
    
    leaderboard_rows = []
    for agent in df["Agent Name"].unique():
        a = df[df["Agent Name"] == agent]
        
        dept = a["Department"].mode()[0] if len(a["Department"].mode()) > 0 else "Unknown"
        
        inbound = a[a["Call Type"] == "inbound"]
        inbound_total = len(inbound)
        inbound_answered = len(inbound[inbound["Call Status"] == "ANSWERED"])
        inbound_rate = (inbound_answered / inbound_total * 100) if inbound_total else 0
        
        outbound = a[a["Call Type"] == "outbound"]
        outbound_total = len(outbound)
        outbound_answered = len(outbound[outbound["Call Status"] == "ANSWERED"])
        outbound_rate = (outbound_answered / outbound_total * 100) if outbound_total else 0
        
        leaderboard_rows.append({
            "Agent Name": agent,
            "Department": dept,
            "Inbound Calls": inbound_total,
            "Inbound Answer Rate (%)": round(inbound_rate, 1),
            "Outbound Calls": outbound_total,
            "Outbound Answer Rate (%)": round(outbound_rate, 1)
        })
    
    leaderboard_table = pd.DataFrame(leaderboard_rows).sort_values("Inbound Answer Rate (%)", ascending=False).reset_index(drop=True)
    leaderboard_table.insert(0, "Rank", range(1, len(leaderboard_table)+1))
    st.markdown(leaderboard_table.to_html(index=False), unsafe_allow_html=True)
    
    st.session_state.overall_table = overall_table
    st.session_state.leaderboard_table = leaderboard_table

# =========================
# PAGE 4: RANKINGS
# =========================
elif st.session_state.page == 'rankings':
    st.header("📥📤 Inbound & Outbound Agent Rankings")
    
    st.subheader("📥 Inbound Ranking")
    inbound_df = df[df["Call Type"]=="inbound"]
    if len(inbound_df):
        inbound_table = build_agent_table(inbound_df)
        st.markdown(inbound_table.to_html(index=False), unsafe_allow_html=True)
        st.session_state.inbound_table = inbound_table
    else:
        st.info("No inbound calls found")
    
    st.markdown("---")
    
    st.subheader("📤 Outbound Ranking")
    outbound_df = df[df["Call Type"]=="outbound"]
    if len(outbound_df):
        outbound_table = build_agent_table(outbound_df)
        st.markdown(outbound_table.to_html(index=False), unsafe_allow_html=True)
        st.session_state.outbound_table = outbound_table
    else:
        st.info("No outbound calls found")

# =========================
# PAGE 5: DURATION
# =========================
elif st.session_state.page == 'duration':
    st.header("⏱️ Call Duration Analysis")
    
    # Duration Analysis (moved from Overview)
    st.subheader("📊 Call Duration Distribution")
    
    order = [
        "0-30 sec", "30 sec-1 min", "1-2 min", "3-5 min",
        "5-10 min", "10-20 min", "20-30 min", "30+ min"
    ]
    duration_counts = df["duration_category"].value_counts().reindex(order, fill_value=0)
    
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(x=duration_counts.index, y=duration_counts.values, text=duration_counts.values,
                     title="Call Duration Distribution")
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(values=duration_counts.values, names=duration_counts.index,
                     title="Call Duration Breakdown")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(pd.DataFrame({
        "Duration Range": duration_counts.index,
        "Calls": duration_counts.values,
        "Percentage": (duration_counts.values/len(df)*100).round(1).astype(str)+"%"
    }).to_html(index=False), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Date-wise Analysis
    st.header("📅 Date-wise Call Duration Analysis")
    
    # Extract date from datetime
    df['date'] = df['Call Date time'].dt.date
    
    duration_rows = []
    for date in sorted(df['date'].unique()):
        day_data = df[df['date'] == date]
        
        # Inbound calls
        inbound = day_data[day_data["Call Type"] == "inbound"]
        inbound_total = len(inbound)
        inbound_answered = len(inbound[inbound["Call Status"] == "ANSWERED"])
        inbound_duration_mins = inbound["duration_minutes"].sum()
        inbound_hours = int(inbound_duration_mins // 60)
        inbound_mins = int(inbound_duration_mins % 60)
        inbound_rate = (inbound_answered / inbound_total * 100) if inbound_total else 0
        
        # Outbound calls
        outbound = day_data[day_data["Call Type"] == "outbound"]
        outbound_total = len(outbound)
        outbound_answered = len(outbound[outbound["Call Status"] == "ANSWERED"])
        outbound_duration_mins = outbound["duration_minutes"].sum()
        outbound_hours = int(outbound_duration_mins // 60)
        outbound_mins = int(outbound_duration_mins % 60)
        outbound_rate = (outbound_answered / outbound_total * 100) if outbound_total else 0
        
        # Total
        total_duration_mins = day_data["duration_minutes"].sum()
        total_hours = int(total_duration_mins // 60)
        total_mins = int(total_duration_mins % 60)
        
        total_answered = len(day_data[day_data["Call Status"] == "ANSWERED"])
        total_calls = len(day_data)
        overall_rate = (total_answered / total_calls * 100) if total_calls else 0
        
        duration_rows.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Total Inbound": inbound_total,
            "Inbound Duration": f"{inbound_hours}h {inbound_mins}m",
            "Inbound Answer Rate (%)": round(inbound_rate, 1),
            "Total Outbound": outbound_total,
            "Outbound Duration": f"{outbound_hours}h {outbound_mins}m",
            "Outbound Answer Rate (%)": round(outbound_rate, 1),
            "Total Calls": total_calls,
            "Total Duration": f"{total_hours}h {total_mins}m",
            "Overall Answer Rate (%)": round(overall_rate, 1)
        })
    
    duration_table = pd.DataFrame(duration_rows)
    st.markdown(duration_table.to_html(index=False), unsafe_allow_html=True)
    
    st.session_state.duration_table = duration_table
    
    st.markdown("---")
    
    st.header("📊 Final Summary Table")
    
    summary_rows = []
    for agent in df["Agent Name"].unique():
        a = df[df["Agent Name"] == agent]
        
        dept = a["Department"].mode()[0] if len(a["Department"].mode()) > 0 else "Unknown"
        
        inbound = a[a["Call Type"] == "inbound"]
        inbound_answered = len(inbound[inbound["Call Status"] == "ANSWERED"])
        inbound_not_answered = len(inbound[inbound["Call Status"] == "NO ANSWER"])
        inbound_busy = len(inbound[inbound["Call Status"] == "BUSY"])
        inbound_failed = len(inbound[inbound["Call Status"] == "FAILED"])
        inbound_total = len(inbound)
        inbound_rate = (inbound_answered / inbound_total * 100) if inbound_total else 0
        
        outbound = a[a["Call Type"] == "outbound"]
        outbound_answered = len(outbound[outbound["Call Status"] == "ANSWERED"])
        outbound_not_answered = len(outbound[outbound["Call Status"] == "NO ANSWER"])
        outbound_busy = len(outbound[outbound["Call Status"] == "BUSY"])
        outbound_failed = len(outbound[outbound["Call Status"] == "FAILED"])
        outbound_total = len(outbound)
        outbound_rate = (outbound_answered / outbound_total * 100) if outbound_total else 0
        
        summary_rows.append({
            "Agent Name": agent,
            "Department": dept,
            "Inbound Answer": inbound_answered,
            "Inbound Not Answer": inbound_not_answered,
            "Outbound Answer": outbound_answered,
            "Outbound Not Answer": outbound_not_answered,
            "Busy": inbound_busy + outbound_busy,
            "Failed": inbound_failed + outbound_failed,
            "Inbound Answer Rate (%)": round(inbound_rate, 1),
            "Inbound Not Answer Rate (%)": round(100 - inbound_rate, 1) if inbound_total else 0,
            "Outbound Answer Rate (%)": round(outbound_rate, 1),
            "Outbound Not Answer Rate (%)": round(100 - outbound_rate, 1) if outbound_total else 0
        })
    
    summary_table = pd.DataFrame(summary_rows)
    st.markdown(summary_table.to_html(index=False), unsafe_allow_html=True)
    
    st.session_state.summary_table = summary_table

# =========================
# PAGE 6: SUMMARY
# =========================
elif st.session_state.page == 'summary':
    st.header("📝 Summary Report")
    
    # Calculate overall statistics
    total_calls = len(df)
    
    # Inbound stats
    inbound_df = df[df["Call Type"] == "inbound"]
    inbound_total = len(inbound_df)
    inbound_answered = len(inbound_df[inbound_df["Call Status"] == "ANSWERED"])
    inbound_unanswered = len(inbound_df[inbound_df["Call Status"] == "NO ANSWER"])
    
    # Outbound stats
    outbound_df = df[df["Call Type"] == "outbound"]
    outbound_total = len(outbound_df)
    outbound_answered = len(outbound_df[outbound_df["Call Status"] == "ANSWERED"])
    outbound_unanswered = len(outbound_df[outbound_df["Call Status"] == "NO ANSWER"])
    
    # Busy and Failed calls
    busy_calls = len(df[df["Call Status"] == "BUSY"])
    failed_calls = len(df[df["Call Status"] == "FAILED"])
    
    # Create Summary Section 1
    summary_section1 = pd.DataFrame({
        "Total calls Inbound/Outbound": [f"{inbound_total}/{outbound_total}"],
        "Total Answered (Inbound/Outbound)": [f"{inbound_answered}/{outbound_answered}"],
        "Total Unanswered (Inbound/Outbound)": [f"{inbound_unanswered}/{outbound_unanswered}"],
        "Busy (Outbound)": [busy_calls],
        "Failed (Outbound)": [failed_calls]
    })
    
    # Create Summary Section 2
    summary_section2 = pd.DataFrame({
        "": ["Total Inbound", "", "Total Outbound", ""],
        " ": ["Answered", "Unanswered", "Answered", "Unanswered"]
    })
    
    # Create Summary Section 3
    summary_section3 = pd.DataFrame({
        "Metric": ["Inbound Answered", "Inbound Not Answered", "Outbound Answered", 
                   "Outbound Not Answered", "Busy Calls", "Failed Calls"],
        "Count": [inbound_answered, inbound_unanswered, outbound_answered, 
                  outbound_unanswered, busy_calls, failed_calls],
        "Percentage": [
            f"{(inbound_answered/total_calls*100):.1f}%" if total_calls else "0.0%",
            f"{(inbound_unanswered/total_calls*100):.1f}%" if total_calls else "0.0%",
            f"{(outbound_answered/total_calls*100):.1f}%" if total_calls else "0.0%",
            f"{(outbound_unanswered/total_calls*100):.1f}%" if total_calls else "0.0%",
            f"{(busy_calls/total_calls*100):.1f}%" if total_calls else "0.0%",
            f"{(failed_calls/total_calls*100):.1f}%" if total_calls else "0.0%"
        ]
    })
    
    # Create Agent Performance Table
    agent_performance_rows = []
    for agent in df["Agent Name"].unique():
        a = df[df["Agent Name"] == agent]
        
        dept = a["Department"].mode()[0] if len(a["Department"].mode()) > 0 else "Unknown"
        
        # Inbound
        inbound = a[a["Call Type"] == "inbound"]
        inbound_duration_mins = inbound["duration_minutes"].sum()
        inbound_hours = int(inbound_duration_mins // 60)
        inbound_mins = int(inbound_duration_mins % 60)
        
        # Outbound
        outbound = a[a["Call Type"] == "outbound"]
        outbound_duration_mins = outbound["duration_minutes"].sum()
        outbound_hours = int(outbound_duration_mins // 60)
        outbound_mins = int(outbound_duration_mins % 60)
        
        # Total
        total_duration_mins = a["duration_minutes"].sum()
        total_hours = int(total_duration_mins // 60)
        total_mins = int(total_duration_mins % 60)
        
        agent_performance_rows.append({
            "Agent Name": agent,
            "Department": dept,
            "Inbound Duration": f"{inbound_hours}h {inbound_mins}m",
            "Outbound Duration": f"{outbound_hours}h {outbound_mins}m",
            "Total Calls": len(a),
            "Total Duration": f"{total_hours}h {total_mins}m",
            "Sort_Minutes": total_duration_mins
        })
    
    agent_performance = pd.DataFrame(agent_performance_rows).sort_values("Sort_Minutes", ascending=False).reset_index(drop=True)
    agent_performance = agent_performance.drop(columns=["Sort_Minutes"])
    agent_performance.insert(0, "Rank", range(1, len(agent_performance)+1))
    
    # Display Preview
    st.subheader("📊 Summary Overview")
    st.markdown(summary_section1.to_html(index=False), unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📋 Call Status Breakdown")
    st.markdown(summary_section3.to_html(index=False), unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🏆 Agent Performance Summary")
    st.markdown(agent_performance.to_html(index=False), unsafe_allow_html=True)
    
    # Create Excel file with all sections
    from io import BytesIO
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Write Section 1
        summary_section1.to_excel(writer, sheet_name='Summary', index=False, startrow=0)
        
        # Write Section 2 (headers)
        summary_section2.to_excel(writer, sheet_name='Summary', index=False, startrow=3, header=False)
        
        # Write Section 3
        summary_section3.to_excel(writer, sheet_name='Summary', index=False, startrow=8)
        
        # Write Agent Performance
        agent_performance.to_excel(writer, sheet_name='Summary', index=False, startrow=17)
    
    excel_data = output.getvalue()
    
    st.markdown("---")
    st.download_button(
        label="📥 Download Summary Report (Excel)",
        data=excel_data,
        file_name=f"summary_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# =========================
# PAGE 7: EXPORT
# =========================
elif st.session_state.page == 'export':
    st.header("💾 Export Data")
    
    st.info("Download any of the following reports:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'overall_table' in st.session_state:
            st.download_button(
                "📥 Download Overall Agent Ranking",
                st.session_state.overall_table.to_csv(index=False),
                f"overall_agent_ranking_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
        
        if 'inbound_table' in st.session_state:
            st.download_button(
                "📥 Download Inbound Ranking",
                st.session_state.inbound_table.to_csv(index=False),
                f"inbound_agent_ranking_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
        
        if 'outbound_table' in st.session_state:
            st.download_button(
                "📥 Download Outbound Ranking",
                st.session_state.outbound_table.to_csv(index=False),
                f"outbound_agent_ranking_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
    
    with col2:
        if 'summary_table' in st.session_state:
            st.download_button(
                "📥 Download Summary Table",
                st.session_state.summary_table.to_csv(index=False),
                f"summary_table_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
        
        if 'duration_table' in st.session_state:
            st.download_button(
                "📥 Download Total Duration Table",
                st.session_state.duration_table.to_csv(index=False),
                f"total_duration_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
        
        if 'leaderboard_table' in st.session_state:
            st.download_button(
                "📥 Download Agent Leaderboard",
                st.session_state.leaderboard_table.to_csv(index=False),
                f"agent_leaderboard_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
    
    st.markdown("---")
    
    st.subheader("📋 Full Call Data")
    st.download_button(
        "📥 Download Complete Call Logs",
        df.to_csv(index=False),
        f"call_logs_{datetime.now().strftime('%Y%m%d')}.csv",
        "text/csv"
    )
    
    st.success("✅ All reports are ready for download!")