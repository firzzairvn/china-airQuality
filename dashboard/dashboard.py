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
st.sidebar.markdown(f"**Nama:** Muhammad Irvan Arfirza")
st.sidebar.markdown(f"**Email:** firzzairvn@gmail.com")
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
    
    
    st.markdown("**1. Pola Musiman**")
    order = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
    # Reindex hanya jika datanya ada
    season_df = main_df.groupby('season')['PM2.5'].mean().reindex(order).reset_index()
        
    fig_season, ax_season = plt.subplots(figsize=(10, 6))
    sns.barplot(data=season_df, x='season', y='PM2.5', palette='rocket', ax=ax_season)
    ax_season.set_xticklabels(ax_season.get_xticklabels(), rotation=45)
    st.pyplot(fig_season)
    st.markdown(
    """
    **Conclusion**: Analisis pola musiman menunjukkan bahwa **Musim Semi** dan **Musim Dingin** merupakan periode dengan risiko tertinggi, di mana rata-rata konsentrasi PM2.5 memuncak di kisaran **70 µg/m³**. Sebaliknya, kualitas udara cenderung membaik secara signifikan saat memasuki **Musim Panas**.
    """
    )

    st.markdown("**2. Pola Harian (Jam)**")
    daily_df = main_df.groupby('hour')['PM2.5'].mean()
    fig_daily, ax_daily = plt.subplots(figsize=(15, 6))
    sns.lineplot(x=daily_df.index, y=daily_df.values, marker='o', color='skyblue', ax=ax_daily)
    ax_daily.set_xlabel("Jam (0-23)")
    st.pyplot(fig_daily)
    st.markdown(
        """
        **Conclusion**: Pola harian menunjukkan tren yang jelas di mana tingkat polusi udara **memuncak pada malam hari** (pukul 21.00 - 23.00) dengan rata-rata di atas 72 µg/m³. Kualitas udara cenderung membaik secara bertahap sejak pagi dan mencapai **kondisi terbaiknya pada sore hari** (pukul 15.00 - 16.00) sebelum kembali memburuk saat aktivitas malam dimulai.
        """
    )
        
    st.markdown("**3. Pola Bulanan**")
    monthly_df = main_df.groupby('month_name')['PM2.5'].mean()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    monthly_df = monthly_df.reindex(month_order)
    
    fig_month, ax_month = plt.subplots(figsize=(12, 4))
    sns.lineplot(x=monthly_df.index, y=monthly_df.values, marker='o', color='salmon', ax=ax_month)
    ax_month.tick_params(axis='x', rotation=45)
    st.pyplot(fig_month)
    st.markdown(
        """
        **Conclusion**: Analisis bulanan mengungkapkan bahwa tingkat polusi udara mencapai puncaknya pada bulan **Maret** dan **November** dengan konsentrasi rata-rata mendekati 78 µg/m³. Sebaliknya, kondisi udara paling bersih (minimum) tercatat pada bulan **Agustus** (sekitar 53 µg/m³), menunjukkan pola musiman yang kuat di mana polusi meningkat drastis pada awal dan akhir tahun.
        """
    )

# TAB 3: Kategori (Pie Chart)
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

# TAB 4: Peta Geografis
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
