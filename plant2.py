import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Crop Production by Region and Year", layout="wide")
st.title("🌾 Crop Production by Region and Year")

uploaded_file = st.file_uploader("📁 Upload CSV File", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file, encoding="utf-8")

    # Extract column headers and data
    data = df_raw[1:].copy()
    data.columns = df_raw.iloc[0]
    data = data.rename(columns={data.columns[0]: "Region"})

    # Select only production columns (those ending in .1)
    prod_cols = [col for col in data.columns if str(col).endswith(".1")]
    years = [col.split(".")[0] for col in prod_cols]  # e.g. "1998"

    # Reformat data for plotting
    all_data = []

    for year, col in zip(years, prod_cols):
        if col in data.columns:
            temp = data[["Region", col]].copy()
            temp.columns = ["Region", "Production"]
            temp["Year"] = year
            all_data.append(temp)

    if all_data:
        df_plot = pd.concat(all_data, ignore_index=True)
    else:
        st.error("❌ No production columns found.")
        st.stop()

    # Convert to numeric
    df_plot["Production"] = pd.to_numeric(df_plot["Production"].astype(str).str.replace(",", ""), errors="coerce")
    df_plot.dropna(subset=["Production"], inplace=True)
    df_plot["Year"] = df_plot["Year"].astype(str)

    # Plotly bar chart
    st.subheader("📊 Production by Region and Year")
    fig = px.bar(
        df_plot,
        x="Year",
        y="Production",
        color="Region",
        barmode="group",
        title="Rice Production by Region Over Time",
        labels={"Year": "Year", "Production": "Production (tons)", "Region": "Region"},
    )
    fig.update_layout(
        xaxis=dict(type="category"),
        yaxis_title="Production (tons)",
        hovermode="x unified",
        xaxis_rangeslider=dict(visible=True)
    )

    st.plotly_chart(fig, use_container_width=True)

    # Optional: show preview
    with st.expander("📄 Preview Data"):
        st.dataframe(df_plot.head(20))

else:
    st.info("👆 Please upload a CSV file.")
