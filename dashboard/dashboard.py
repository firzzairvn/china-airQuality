# import streamlit as st
# import pandas as pd
# import folium
# import seaborn as sns
# import matplotlib.pyplot as plt
# from streamlit_folium import st_folium

# from data_preprocessing import load_and_preprocess_data, get_color, station_coordinates, get_season, categorize_pm25

# st.set_page_config(
#     page_title="Air Quality Dashboard",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Load data
# with st.spinner('Loading and preprocessing data... This might take a moment.'):
#     df_pm25 = load_and_preprocess_data()

# #Sidebar
# st.sidebar.title("Air Quality Dashboard")
# st.sidebar.info("This dashboard visualizes PM2.5 concentrations across various stations, daily, monthly, and seasonal patterns, and air quality categories.")

# #Title
# st.title("Air Quality Analysis in China")


# st.subheader("1. Areas with Highest Risk (Geographic Map)")

# if not df_pm25.empty:
#     avgpm25_perStation_map_data = df_pm25.groupby('station').agg(
#         avg_PM2_5=('PM2.5', 'mean'),
#         latitude=('latitude', 'first'),
#         longitude=('longitude', 'first')
#     ).reset_index()

#     center_lat = avgpm25_perStation_map_data['latitude'].mean() if not avgpm25_perStation_map_data['latitude'].isnull().all() else 39.9
#     center_lon = avgpm25_perStation_map_data['longitude'].mean() if not avgpm25_perStation_map_data['longitude'].isnull().all() else 116.4

#     folium_map = folium.Map(
#         location=[center_lat, center_lon],
#         zoom_start=6
#     )

#     for index, row in avgpm25_perStation_map_data.iterrows():
#         lat = row['latitude']
#         lon = row['longitude']
#         station_name = row['station']
#         avg_pm25 = row['avg_PM2_5']

#         if pd.isna(lat) or pd.isna(lon) or pd.isna(avg_pm25):
#             continue

#         color = get_color(avg_pm25)
#         radius = (avg_pm25 / 10) + 5

#         folium.CircleMarker(
#             location=[lat, lon],
#             radius=radius,
#             color=color,
#             fill=True,
#             fill_color=color,
#             fill_opacity=0.7,
#             tooltip=f"Station: {station_name}<br>Avg PM2.5: {avg_pm25:.2f} \u00B5g/m\u00B3<br>Category: {categorize_pm25(avg_pm25)}",
#         ).add_to(folium_map)

#     st_folium(folium_map, width=1000, height=500)
# else:
#     st.warning("No data available to display the map.")

# # --- Question 1 ----
# st.subheader("Highest Risk Areas by PM2.5 Concentration")

# if not df_pm25.empty:
#     avgpm25_perStation = df_pm25.groupby('station')['PM2.5'].mean().sort_values(ascending=False)

#     fig, ax = plt.subplots(figsize=(12, 6))
#     sns.barplot(x=avgpm25_perStation.index, y=avgpm25_perStation.values, palette='viridis', ax=ax)
#     ax.set_title('Average PM2.5 Concentration per Station (\u00B5g/m\u00B3)')
#     ax.set_xlabel('Station')
#     ax.set_ylabel('Average PM2.5 (\u00B5g/m\u00B3)')
#     ax.tick_params(axis='x', rotation=45)
#     st.pyplot(fig)
# else:
#     st.warning("No data available to display 'Highest Risk Areas' bar chart.")


# # --- Question 2 ---
# st.subheader("2. PM2.5 Air Quality Patterns Over Time")

# if not df_pm25.empty:
#     st.markdown("### Daily Pattern")
#     daily_pm25_pattern = df_pm25.groupby('hour')['PM2.5'].mean()
#     fig_daily, ax_daily = plt.subplots(figsize=(12, 6))
#     sns.lineplot(x=daily_pm25_pattern.index, y=daily_pm25_pattern.values, marker='o', color='skyblue', ax=ax_daily)
#     ax_daily.set_title('Daily Pattern of PM2.5 Concentration')
#     ax_daily.set_xlabel('Hour of Day')
#     ax_daily.set_ylabel('Average PM2.5 (\u00B5g/m\u00B3)')
#     ax_daily.set_xticks(range(0, 24))
#     ax_daily.grid(False)
#     st.pyplot(fig_daily)

#     st.markdown("### Monthly Pattern")
#     monthly_pm25_pattern = df_pm25.groupby('month_name')['PM2.5'].mean()
#     month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#     monthly_pm25_pattern = monthly_pm25_pattern.reindex(month_order)
#     fig_monthly, ax_monthly = plt.subplots(figsize=(12, 6))
#     sns.lineplot(x=monthly_pm25_pattern.index, y=monthly_pm25_pattern.values, marker='o', color='salmon', ax=ax_monthly)
#     ax_monthly.set_title('Monthly Pattern of PM2.5 Concentration')
#     ax_monthly.set_xlabel('Month')
#     ax_monthly.set_ylabel('Average PM2.5 (\u00B5g/m\u00B3)')
#     ax_monthly.tick_params(axis='x', rotation=45)
#     ax_monthly.grid(False)
#     st.pyplot(fig_monthly)

#     st.markdown("### Seasonal Pattern")
#     seasonal_pm25_pattern = df_pm25.groupby('season')['PM2.5'].mean()
#     season_order = ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'] 
#     seasonal_pm25_pattern = seasonal_pm25_pattern.reindex(season_order)
#     fig_seasonal, ax_seasonal = plt.subplots(figsize=(10, 6))
#     sns.barplot(x=seasonal_pm25_pattern.index, y=seasonal_pm25_pattern.values, palette='coolwarm', ax=ax_seasonal)
#     ax_seasonal.set_title('Seasonal Pattern of PM2.5 Concentration')
#     ax_seasonal.set_xlabel('Season')
#     ax_seasonal.set_ylabel('Average PM2.5 (\u00B5g/m\u00B3)')
#     st.pyplot(fig_seasonal)
# else:
#     st.warning("No data available to display 'Air Quality Patterns' charts.")


# # --- Question 3 ---
# st.subheader("3. Frequency of Unhealthy Air Quality Days (PM2.5 Categories)")

# if not df_pm25.empty:
#     pm25_catPercentages = df_pm25['PM2.5_category'].value_counts(normalize=True) * 100


#     category_order = ['Baik', 'Sedang', 'Tidak Sehat (Sensitif)', 'Tidak Sehat', 'Sangat Tidak Sehat']
#     pm25_catPercentages = pm25_catPercentages.reindex(category_order, fill_value=0)

#     fig_cat, ax_cat = plt.subplots(figsize=(10, 6))
#     sns.barplot(x=pm25_catPercentages.index, y=pm25_catPercentages.values, palette='RdYlGn_r', ax=ax_cat)
#     ax_cat.set_title('Distribution of PM2.5 Air Quality Categories')
#     ax_cat.set_xlabel('Air Quality Category')
#     ax_cat.set_ylabel('Percentage (%)')
#     ax_cat.tick_params(axis='x', rotation=45)
#     st.pyplot(fig_cat)


#     unhealthy_categories = ['Tidak Sehat (Sensitif)', 'Tidak Sehat', 'Sangat Tidak Sehat']
#     unhealthy_percentage = pm25_catPercentages[pm25_catPercentages.index.isin(unhealthy_categories)].sum()
#     st.markdown(f"**Conclusion**: Approximately **{unhealthy_percentage:.2f}%** of the time, the air quality falls into an 'Unhealthy' category based on PM2.5 standards.")
# else:
#     st.warning("No data available to display 'PM2.5 Category Proportions' chart.")

""" Layout Lama: """
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium

# Import fungsi dari modul data_preprocessing Anda yang sudah diperbaiki
from data_preprocessing import load_and_preprocess_data, get_color, categorize_pm25

# --- 1. CONFIG ---
st.set_page_config(
    page_title="Air Quality Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
# Menggunakan fungsi dari data_preprocessing.py agar data otomatis terbaca
with st.spinner('Memuat dan memproses data...'):
    df = load_and_preprocess_data()

# --- 3. SIDEBAR FILTER (Layout Lama) ---
st.sidebar.title("Air Quality Dashboard")
st.sidebar.markdown(f"**Nama:** Muhammad Irvan Arfirza\n**Email:** firzzairvn@gmail.com")
st.sidebar.markdown("---")
st.sidebar.header("Filter Data")

# Pastikan data tidak kosong sebelum membuat filter
if not df.empty:
    station_list = df["station"].unique()
    selected_station = st.sidebar.multiselect(
        "Pilih Stasiun:",
        options=station_list,
        default=station_list # Default terpilih semua
    )

    # Filter DataFrame berdasarkan pilihan
    if not selected_station:
        st.warning("Mohon pilih minimal satu stasiun di sidebar.")
        st.stop()
    
    main_df = df[df["station"].isin(selected_station)]
else:
    st.error("Data tidak ditemukan. Pastikan file CSV ada.")
    st.stop()

# --- 4. MAIN LAYOUT (Metrics & Title) ---
st.title("📊 Air Quality Analysis in China")
st.markdown("---")

# Kolom Metrik (Layout Lama)
col1, col2, col3 = st.columns(3)
with col1:
    avg_pm25 = main_df['PM2.5'].mean()
    st.metric("Rerata PM2.5", f"{avg_pm25:.2f} µg/m³")
with col2:
    max_pm25 = main_df['PM2.5'].max()
    st.metric("Max PM2.5", f"{max_pm25:.2f} µg/m³")
with col3:
    # Menghitung jumlah kategori tidak sehat
    unhealthy_counts = main_df[main_df['PM2.5_category'].isin(['Tidak Sehat', 'Sangat Tidak Sehat'])].shape[0]
    st.metric("Total Data Tidak Sehat", f"{unhealthy_counts}")

st.markdown("---")

# --- 5. TABS VISUALISASI (Layout Lama) ---
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Analisis Lokasi", "📈 Tren Waktu", "🍩 Kategori", "🌍 Peta Persebaran"])

# TAB 1: Analisis Lokasi (Bar Chart)
with tab1:
    st.subheader("Daerah dengan Risiko Tertinggi")
    
    # Grouping data
    risk_data = main_df.groupby("station")["PM2.5"].mean().sort_values(ascending=False).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="PM2.5", y="station", data=risk_data, palette="Reds_r", ax=ax)
    ax.set_xlabel("Rata-rata PM2.5 (µg/m³)")
    ax.set_ylabel("Stasiun")
    ax.set_title("Rata-rata Tingkat Polusi per Stasiun")
    st.pyplot(fig)

# TAB 2: Tren Waktu (Menggabungkan Seasonal, Daily, Monthly)
with tab2:
    st.subheader("Pola Kualitas Udara")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**1. Pola Musiman**")
        order = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
        # Reindex hanya jika datanya ada
        season_df = main_df.groupby('season')['PM2.5'].mean().reindex(order).reset_index()
        
        fig_season, ax_season = plt.subplots(figsize=(6, 4))
        sns.barplot(data=season_df, x='season', y='PM2.5', palette='coolwarm', ax=ax_season)
        ax_season.set_xticklabels(ax_season.get_xticklabels(), rotation=45)
        st.pyplot(fig_season)

    with col_b:
        st.markdown("**2. Pola Harian (Jam)**")
        daily_df = main_df.groupby('hour')['PM2.5'].mean()
        fig_daily, ax_daily = plt.subplots(figsize=(6, 4))
        sns.lineplot(x=daily_df.index, y=daily_df.values, marker='o', color='skyblue', ax=ax_daily)
        ax_daily.set_xlabel("Jam (0-23)")
        st.pyplot(fig_daily)
        
    st.markdown("**3. Pola Bulanan**")
    monthly_df = main_df.groupby('month_name')['PM2.5'].mean()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    monthly_df = monthly_df.reindex(month_order)
    
    fig_month, ax_month = plt.subplots(figsize=(12, 4))
    sns.lineplot(x=monthly_df.index, y=monthly_df.values, marker='o', color='salmon', ax=ax_month)
    ax_month.tick_params(axis='x', rotation=45)
    st.pyplot(fig_month)

# TAB 3: Kategori (Pie Chart - Sesuai layout lama)
with tab3:
    st.subheader("Proporsi Kategori Udara")
    
    cat_counts = main_df['PM2.5_category'].value_counts()
    
    # Warna custom agar sesuai konteks (Hijau=Baik, Merah=Bahaya)
    # Kita buat mapping sederhana, jika kategori tidak ada di list, biarkan otomatis
    colors_map = {
        'Baik': '#66c2a5', 
        'Sedang': '#ffffb3', 
        'Tidak Sehat (Sensitif)': '#fdae61', 
        'Tidak Sehat': '#f46d43', 
        'Sangat Tidak Sehat': '#d53e4f'
    }
    chart_colors = [colors_map.get(x, '#cccccc') for x in cat_counts.index]

    fig_pie, ax_pie = plt.subplots(figsize=(8, 8))
    ax_pie.pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%', startangle=90, colors=chart_colors)
    ax_pie.set_title("Distribusi Kategori PM2.5")
    st.pyplot(fig_pie)
    
    # Penjelasan singkat
    st.info("Kategori ditentukan berdasarkan standar ambang batas PM2.5.")

# TAB 4: Peta Geografis (Logic Baru dengan Tampilan Peta)
with tab4:
    st.subheader("Peta Persebaran Stasiun")
    st.write("Warna dan ukuran lingkaran menunjukkan tingkat rata-rata PM2.5.")

    # Agregasi data untuk peta (menggunakan main_df yang sudah difilter)
    map_data = main_df.groupby('station').agg(
        avg_PM2_5=('PM2.5', 'mean'),
        latitude=('latitude', 'first'),
        longitude=('longitude', 'first')
    ).reset_index()

    # Drop data yang tidak punya koordinat
    map_data = map_data.dropna(subset=['latitude', 'longitude'])

    if not map_data.empty:
        # Tentukan tengah peta
        center_lat = map_data['latitude'].mean()
        center_lon = map_data['longitude'].mean()

        m = folium.Map(location=[center_lat, center_lon], zoom_start=9)

        for _, row in map_data.iterrows():
            # Menggunakan helper function get_color yang diimport
            color = get_color(row['avg_PM2_5'])
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=(row['avg_PM2_5'] / 10) + 5, # Ukuran dinamis
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                tooltip=f"<b>{row['station']}</b><br>PM2.5: {row['avg_PM2_5']:.2f} µg/m³"
            ).add_to(m)

        st_folium(m, width=1000, height=500)
    else:
        st.warning("Tidak ada data lokasi yang valid untuk ditampilkan di peta.")