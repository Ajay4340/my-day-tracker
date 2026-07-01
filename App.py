import streamlit as st
import pandas as pd
import plotly.express as px

# Mobile-friendly page config
st.set_page_config(page_title="Day Tracker", page_icon="⏱️", layout="centered")

st.title("⏱️ Hourly Daily Tracker")

CATEGORIES = ["Deep Work", "Shallow Work", "Learning", "Exercise", "Chores/Logistics", "Breaks/Leisure", "Sleep", "Custom"]
HOURS = [f"{i:02d}:00 - {i+1:02d}:00" for i in range(24)]

if "tracker_data" not in st.session_state:
    st.session_state.tracker_data = {slot: {"category": "Sleep", "details": ""} for slot in HOURS}

# Sidebar for controls
with st.sidebar:
    st.header("Controls")
    bulk_cat = st.selectbox("Bulk Assign", ["None"] + CATEGORIES)
    if bulk_cat != "None" and st.button("Apply to All"):
        for slot in HOURS:
            st.session_state.tracker_data[slot]["category"] = bulk_cat
    if st.button("Reset Day", type="primary"):
        st.session_state.tracker_data = {slot: {"category": "Sleep", "details": ""} for slot in HOURS}

st.subheader("🗓️ Log Your Hours")
for slot in HOURS:
    current_cat = st.session_state.tracker_data[slot]["category"]
    current_det = st.session_state.tracker_data[slot]["details"]
    idx = CATEGORIES.index(current_cat) if current_cat in CATEGORIES else 0
    
    # Stacked layout optimized for mobile screens
    chosen_cat = st.selectbox(f"Time: {slot}", CATEGORIES, index=idx, key=f"cat_{slot}")
    chosen_det = st.text_input(f"Detail for {slot}", value=current_det, key=f"det_{slot}", placeholder="e.g., Gym, Coding, Nap")
    st.session_state.tracker_data[slot] = {"category": chosen_cat, "details": chosen_det}
    st.markdown("---")

st.subheader("📊 End of Day Summary")
summary_data = [{"Hour": k, "Category": v["category"], "Details": v["details"]} for k, v in st.session_state.tracker_data.items()]
df = pd.DataFrame(summary_data)

df_counts = df["Category"].value_counts().reset_index()
df_counts.columns = ["Category", "Hours Spent"]

productive_cats = ["Deep Work", "Shallow Work", "Learning", "Exercise"]
prod_hours = df[df["Category"].isin(productive_cats)].shape[0]

st.metric(label="🚀 Productive Hours", value=f"{prod_hours} / 24 hrs")

fig = px.pie(df_counts, values="Hours Spent", names="Category", hole=0.3)
fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 View Full Day Log Table"):
    st.dataframe(df, use_container_width=True)
  
