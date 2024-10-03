import streamlit as st
!pip install streamlit pandas matplotlib seaborn
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    days_df = pd.read_csv("day.csv")
    days_df['dteday'] = pd.to_datetime(days_df['dteday'])
    days_df.rename(columns={
        'dteday': 'tanggal',
        'yr': 'tahun',
        'mnth': 'bulan',
        'weathersit': 'cuaca',
        'hum': 'kelembapan',
        'cnt': 'total_penyewaan'
    }, inplace=True)

    # Konversi data kategori
    days_df['musim'] = days_df.season.map({1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'})
    days_df['tahun'] = days_df.tahun.map({0: 2011, 1: 2012})
    days_df['bulan'] = days_df.bulan.map({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                                          7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
    days_df['cuaca'] = days_df.cuaca.map({1: 'Cerah', 2: 'Kabut', 3: 'Hujan Ringan Salju', 4: 'Hujan Berat Salju'})
    days_df['hari'] = days_df.weekday.map({0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu',
                                           4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'})

    # Konversi suhu
    days_df['suhu'] = days_df['temp'] * 41
    days_df['suhu_atemp'] = days_df['atemp'] * 50

    return days_df

# Memuat data
days_df = load_data()

# Judul dashboard
st.title('Dashboard Penyewaan Sepeda🚲')

# Garis horizontal di bawah judul
st.markdown("<hr style='height:2px; background-color:black;'>", unsafe_allow_html=True)

# Sidebar untuk informasi data asli
st.sidebar.header('Informasi Data Asli')
if st.sidebar.checkbox('Tampilkan Data'):
    # Mengubah tampilan suhu menjadi lebih jelas
    days_df['suhu'] = days_df['suhu'].round(2)  # Pembulatan suhu
    days_df['suhu_atemp'] = days_df['suhu_atemp'].round(2)  # Pembulatan suhu atemp
    
    # Pastikan kolom 'tahun' ditampilkan sebagai integer tanpa koma
    days_df['tahun'] = days_df['tahun'].astype(int)
    
    st.sidebar.dataframe(days_df[['tanggal', 'tahun', 'bulan', 'musim', 'cuaca', 'suhu', 'suhu_atemp', 'kelembapan', 'total_penyewaan']])

# Menambahkan filter untuk pemilihan periode waktu
st.sidebar.header("Filter Periode Waktu")
start_date = st.sidebar.date_input("Mulai tanggal", value=pd.to_datetime("2011-01-01"), min_value=pd.to_datetime("2011-01-01"), max_value=pd.to_datetime("2012-12-31"))
end_date = st.sidebar.date_input("Sampai tanggal", value=pd.to_datetime("2012-12-31"), min_value=pd.to_datetime("2011-01-01"), max_value=pd.to_datetime("2012-12-31"))

# Filter data berdasarkan periode waktu
filtered_df = days_df[(days_df['tanggal'] >= pd.to_datetime(start_date)) & (days_df['tanggal'] <= pd.to_datetime(end_date))]

# Insight total penggunaan penyewaan sepeda berdasarkan periode waktu
total_usage = filtered_df['total_penyewaan'].sum()

# Fakta Jumlah
st.header('Fakta Jumlah Penyewaan Sepeda')

# Desain border box yang lebih menarik dengan warna merah dan bayangan
fact_container = st.container()
with fact_container:
    col1, col2, col3, col4, col5 = st.columns(5)  # Membuat 5 kolom untuk fakta
    box_style = """
        <div style='border-radius: 10px; padding: 15px; background: linear-gradient(135deg, #f54242, #e53935);
                    color: white; box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1); text-align: center;
                    transition: transform 0.2s ease;'>
            <style>
                div:hover {
                    transform: scale(1.05);
                }
            </style>
        """
    with col1:
        st.markdown(f"{box_style}<strong>Total Penyewaan:</strong><br>{total_usage}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"{box_style}<strong>Tahun:</strong><br>{int(filtered_df['tahun'].nunique())}</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"{box_style}<strong>Bulan Data:</strong><br>{filtered_df['bulan'].nunique()} bulan</div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"{box_style}<strong>Total Hari:</strong><br>{filtered_df['tanggal'].nunique()} hari</div>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"{box_style}<strong>Cuaca Beragam:</strong><br>{filtered_df['cuaca'].nunique()} jenis cuaca</div>", unsafe_allow_html=True)

# Garis horizontal di bawah judul
st.markdown("---")

# Pertanyaan 1: Total Penyewaan Sepeda per Bulan
st.header('Total Penyewaan Sepeda per Bulan')
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='bulan', y='total_penyewaan', data=filtered_df, hue='tahun', palette=['#f54242', '#f5d142'], ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan")
ax.set_title("Total Penyewaan Sepeda per Bulan")
st.pyplot(fig)

st.write("""*Insight:*
- Total penyewaan sepeda cenderung meningkat pada bulan juni-september tahun 2012.
- Total penyewaan sepeda cenderung meningkat pada bulan april-juni tahun 2011.""")

st.markdown("---")

# Pertanyaan 2: Penggunaan Sepeda Berdasarkan Musim
st.header('Penggunaan Sepeda Berdasarkan Musim')
season_df = days_df.groupby("musim")["total_penyewaan"].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="musim", y="total_penyewaan", data=season_df.sort_values(by="total_penyewaan", ascending=False), 
            palette=['#ff5959', '#ff7961', '#ffcccb'], ax=ax)
ax.set_title("Penggunaan Sepeda Berdasarkan Musim", fontsize=15)
ax.set_ylabel('Jumlah Pengguna Sepeda')
ax.set_xlabel('Musim')
for index, value in enumerate(season_df['total_penyewaan']):
    ax.text(index, value, str(round(value, 2)), ha='center', va='bottom')
st.pyplot(fig)

st.write("""*Insight:*
- Musim panas adalah musim dengan penggunaan sepeda tertinggi.""")

st.markdown("---")

# Pertanyaan 3: Korelasi Suhu dan Penyewaan
st.header('Korelasi antara Suhu dan Total Penyewaan')
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x='suhu', y='total_penyewaan', data=filtered_df, hue='musim', ax=ax)
ax.set_xlabel("Suhu (°C)")
ax.set_ylabel("Total Penyewaan")
ax.set_title("Korelasi Suhu dan Penyewaan Sepeda")
st.pyplot(fig)

st.write("""*Insight:*
- Semakin tinggi suhu maka semakin tinggi jumlah penyewaan sepeda.""")

st.markdown("---")

# Kesimpulan
st.header('Kesimpulan')
st.write("""
1. Total penyewaan sepeda bervariasi berdasarkan bulan dan musim.
2. Musim panas menunjukkan penggunaan tertinggi dibandingkan dengan musim lainnya.
3. Suhu yang lebih tinggi cenderung berhubungan dengan jumlah penyewaan yang lebih banyak.
""")

