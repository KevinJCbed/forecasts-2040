import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Export Forecast Visualization by Country")

# Upload Excel files
merch_file = st.file_uploader("Upload Merchandise Exports Forecast Excel File", type=["xlsx"])
services_file = st.file_uploader("Upload Services Exports Forecast Excel File", type=["xlsx"])

if merch_file and services_file:
    # Load data
    merch_df = pd.read_excel(merch_file)
    services_df = pd.read_excel(services_file)

    # Validate data structure
    required_columns = {"iso3_o","iso3_d", "year", "exports", "fitted1", "corrected_pred2"}
    if not required_columns.issubset(merch_df.columns) or not required_columns.issubset(services_df.columns):
        st.error("Both Excel files must have all required columns")
    else:
        # Get list of countries
        countries = sorted(set(merch_df['iso3_d']).intersection(services_df['iso3_d']))
        country = st.selectbox("Select a Country", countries)

        # Filter data by country
        merch_country = merch_df[merch_df['iso3_d'] == country].sort_values("year")
        services_country = services_df[services_df['iso3_d'] == country].sort_values("year")
        
        def plot_with_shading(df, title):
            fig, ax = plt.subplots(figsize=(10, 5))
            years = df["year"]

            ax.plot(years, df["exports"], label="observed exports", marker='o')
            ax.plot(years, df["fitted1"], label="baseline predictions", marker='o', linestyle='--')
            ax.plot(years, df["corrected_pred2"], label="corrected predictions", marker='o', linestyle='--')

            # Shade the area where year > 2020
            ax.axvspan(2020, years.max(), color='gray', alpha=0.3)

            ax.set_title(title)
            ax.set_xlabel("year")
            ax.set_ylabel("exports")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

        # Determine year range from data
        min_year = int(min(merch_country["year"].min(), services_country["year"].min()))
        max_year = int(max(merch_country["year"].max(), services_country["year"].max()))

        # Year range slider
        year_range = st.slider(
            "Select Year Range to Display",
            min_value=min_year,
            max_value=max_year,
            value=(2015, 2040),
            step=1
        )

        # Filter data by selected year range
        start_year, end_year = year_range
        merch_country = merch_country[(merch_country["year"] >= start_year) & (merch_country["year"] <= end_year)]
        services_country = services_country[(services_country["year"] >= start_year) & (services_country["year"] <= end_year)]

        st.subheader(f"Merchandise Export Forecast for {country}")
        plot_with_shading(merch_country, f"Merchandise Exports for {country}")

        st.subheader(f"Services Export Forecast for {country}")
        plot_with_shading(services_country, f"Services Exports for {country}")
else:
    st.info("Please upload both Excel files to proceed.")
