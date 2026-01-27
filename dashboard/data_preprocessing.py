import pandas as pd
import os

station_coordinates = {
    'Aotizhongxin': [25.956934163381177, 117.3681770616395],
    'Changping': [40.22224, 116.24192],
    'Dingling': [40.29285, 116.2259],
    'Dongsi': [39.91632, 116.4164],
    'Gucheng': [26.890965836846178, 100.2620337652272],
    'Guanyuan': [32.433678685529486, 105.84684268266686],
    'Huairou': [40.38601, 116.626],
    'Nongzhanguan': [39.93273, 116.46043],
    'Shunyi': [40.12645, 116.64364],
    'Tiantan': [39.88665, 116.40722],
    'Wanliu': [39.98662, 116.30514],
    'Wanshouxigong': [39.87948, 116.3526],
}


def get_season(month):
    if 3 <= month <= 5:
        return 'Musim Semi'
    elif 6 <= month <= 8:
        return 'Musim Panas'
    elif 9 <= month <= 11:
        return 'Musim Gugur'
    else:
        return 'Musim Dingin'

def categorize_pm25(pm25_value):
    if 0 <= pm25_value <= 12:
        return 'Baik'
    elif 12.1 <= pm25_value <= 35.4:
        return 'Sedang'
    elif 35.5 <= pm25_value <= 55.4:
        return 'Tidak Sehat (Sensitif)'
    elif 55.5 <= pm25_value <= 150.4:
        return 'Tidak Sehat'
    elif pm25_value > 150.4:
        return 'Sangat Tidak Sehat'
    else:
        return 'Tidak Diketahui'

def get_color(pm25_value):
    if pm25_value <= 12:
        return 'green' # Baik
    elif 12.1 <= pm25_value <= 35.4:
        return 'yellow' # Sedang
    elif 35.5 <= pm25_value <= 55.4:
        return 'orange' # Tidak Sehat (Sensitif)
    elif 55.5 <= pm25_value <= 150.4:
        return 'red' # Tidak Sehat
    else:
        return 'darkred' # Sangat Tidak Sehat

def clean_outliers(df, columns):
    initial_rows = df.shape[0]
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        df = df[~((df[col] < lower_bound) | (df[col] > upper_bound))]

    final_rows = df.shape[0]
    print(f"Jumlah data sebelum menghilangkan outlier: {initial_rows} baris")
    print(f"Jumlah data setelah menghilangkan outlier: {final_rows} baris")
    print(f"Total outlier yang dihapus: {initial_rows - final_rows} baris")
    return df


def load_and_preprocess_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # File Path
    file_path = os.path.join(current_dir, 'China_airQuality.csv')
    
    # Check Data
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' tidak ditemukan di direktori ini.")
        return pd.DataFrame()
    
    try:
        print(f"Membaca dataset dari: {file_path}")
        df_pm25 = pd.read_csv(file_path)
        
        # Filter kolom yang dibutuhkan
        df_pm25 = df_pm25[['year', 'month', 'day', 'hour', 'PM2.5', 'station']].copy()

        # Mapping Latitude & Longitude
        df_pm25['latitude'] = df_pm25['station'].map(lambda x: station_coordinates.get(x, [None, None])[0])
        df_pm25['longitude'] = df_pm25['station'].map(lambda x: station_coordinates.get(x, [None, None])[1])

        # Konversi Datetime
        df_pm25['datetime'] = pd.to_datetime(df_pm25[['year', 'month', 'day', 'hour']])
        df_pm25['day_name'] = df_pm25['datetime'].dt.day_name()
        df_pm25['month_name'] = df_pm25['datetime'].dt.month_name()
        
        # Set Index
        df_pm25 = df_pm25.set_index('datetime')

        # Imputasi Missing Values
        df_pm25['PM2.5'] = df_pm25['PM2.5'].ffill().bfill()
        print(f"Missing values in PM2.5 after imputation: {df_pm25['PM2.5'].isnull().sum()}")

        # Bersihkan Outlier
        df_pm25 = clean_outliers(df_pm25.copy(), ['PM2.5'])

        # Tambahkan Fitur Musim dan Kategori
        df_pm25['season'] = df_pm25['month'].apply(get_season)
        df_pm25['PM2.5_category'] = df_pm25['PM2.5'].apply(categorize_pm25)

        # Hitung Rata-rata per Stasiun
        avgpm25_perStation = df_pm25.groupby('station')['PM2.5'].mean().sort_values(ascending=False)
        avgpm25_perStation_df = avgpm25_perStation.reset_index()
        avgpm25_perStation_df.rename(columns={'PM2.5': 'avg_PM2.5'}, inplace=True)
        df_pm25 = pd.merge(df_pm25, avgpm25_perStation_df, on='station', how='left')

        print("Data preprocessing complete.")
        return df_pm25

    except Exception as e:
        print(f"Terjadi kesalahan saat memproses data: {e}")
        return pd.DataFrame()

if __name__ == '__main__':
    processed_df = load_and_preprocess_data()
    print("\nProcessed DataFrame head:")
    print(processed_df.head())