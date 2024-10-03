import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 

sns.set(style='dark')

df = pd.read_csv('Dashboard/data_bersih.csv')


    # grouping buat berdasarkan season dan tahun
seasonal_rentals = df.groupby(['season', 'yr'])['cnt'].sum().reset_index()
sorted_data = seasonal_rentals.sort_values(by='cnt', ascending=False)
    # Menambahkan nama musim untuk kejelasan
seasonal_rentals['season_name'] = seasonal_rentals['season'].replace({1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'})

    # Memisahkan data tahun 2011 dan 2012
rentals_2011 = seasonal_rentals[seasonal_rentals['yr'] == 0].set_index('season')

rentals_2012 = seasonal_rentals[seasonal_rentals['yr'] == 1].set_index('season')

    # Menggabungkan data untuk melihat perubahan dari 2011 ke 2012
merged_rentals = rentals_2011[['cnt']].rename(columns={'cnt': '2011'}).join(rentals_2012[['cnt']].rename(columns={'cnt': '2012'}))

    # Menghitung persentase perubahan dari 2011 ke 2012
merged_rentals['percentage_change'] = ((merged_rentals['2012'] - merged_rentals['2011']) / merged_rentals['2011']) * 100
merged_rentals['percentage'] = merged_rentals['percentage_change'].apply(lambda x: f'{x:.2f}%')

    # Menambahkan nama musim untuk kejelasan
merged_rentals['season_name'] = merged_rentals.index.map({1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'})

# Mengelompokkan data berdasarkan tahun dan menghitung jumlah total penyewaan
yearly_rentals = df.groupby('yr')['cnt'].sum().reset_index()
yearly_rentals['year'] = yearly_rentals['yr'].replace({0: '2011', 1: '2012'})

# Mengambil jumlah penyewaan untuk setiap tahun
count_2011 = yearly_rentals.loc[yearly_rentals['year'] == '2011', 'cnt'].values[0]
count_2012 = yearly_rentals.loc[yearly_rentals['year'] == '2012', 'cnt'].values[0]

# Menghitung persentase perubahan dari 2011 ke 2012
percentage_change = ((count_2012 - count_2011) / count_2011) * 100

#summary pola penyewa sepeda
summary = df.groupby('workingday')['cnt'].sum().reset_index()
summary['workingday'] = summary['workingday'].map({1: 'Hari Kerja', 0: 'Akhir Pekan/Hari Libur'})\

# Menghitung total penyewaan hari kerja dan hari libur
total_workingday = summary[summary['workingday'] == 'Hari Kerja']['cnt'].values[0]
total_holiday = summary[summary['workingday'] == 'Akhir Pekan/Hari Libur']['cnt'].values[0]

# Menghitung persentase perbedaan
percentage_difference = ((total_workingday - total_holiday) / total_holiday) * 100



#yet Another Grouping............................................................

#yet Another Grouping............................................................

# Convert 'yr' to actual year values for easier understanding (2011 and 2012)
df['year'] = df['yr'].replace({0: 2011, 1: 2012})

# Mapping the season to actual names
df['season_name'] = df['season'].replace({1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'})

# Group by season and year to get the total bike rentals
seasonal_rentals = df.groupby(['season_name', 'year'])['cnt'].sum().reset_index()

# Pivot the data to calculate percentage change between 2011 and 2012
rentals_pivot = seasonal_rentals.pivot(index='season_name', columns='year', values='cnt')

# Calculate percentage change between 2011 and 2012
rentals_pivot['percentage_change'] = ((rentals_pivot[2012] - rentals_pivot[2011]) / rentals_pivot[2011]) * 100
rentals_pivot['percentage'] = rentals_pivot['percentage_change'].apply(lambda x: f'{x:.2f}%')

rentals_pivot = rentals_pivot.reset_index()

# Estimate the rentals for 2013 assuming a 10% increase from 2012
rentals_pivot['2013_estimation'] = rentals_pivot[2012] * 1.10




#yet Another Grouping............................................................

#yet Another Grouping............................................................

st.header('Data Analyst of Bike Sharing Consumer over 2011 - 2012')
st.subheader('Total Pengguna Bike Sharing selama 1 tahun')



# Membuat dua kolom untuk menampilkan jumlah penyewaan
col1, col2 = st.columns(2)
with col1:
    st.write('**Tahun 2011**')
    st.metric(label='Total Pengguna :', value=count_2011)

with col2:
    st.write('**Tahun 2012**')
    st.metric(label='Total Pengguna :', value=count_2012)

st.subheader('Presentase Kenaikan dari 2011 ke 2012')
st.metric(label='Dari 2011 ke 2012 :', value=f'{percentage_change:.2f}%', delta=f'{percentage_change:.2f}%')

st.subheader('Kenaikan Berdasarkan Musim')

#plot selisih penyewa permusim selama satu tahun
plt.figure(figsize=(12, 6))
sns.barplot(x='season', y='cnt', hue='yr', data=sorted_data.sort_values(by='cnt', ascending=False), estimator=sum, errorbar=None)
plt.title('Total Penyewaan Sepeda Berdasarkan Musim dan Tahun')
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan')
plt.xticks([0, 1, 2, 3], ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])
plt.legend(title='Tahun', labels=['2011', '2012'])
plt.show()
st.pyplot(plt)

st.subheader('Presentase Kenaikan Berdasarkan Musim')
st.table(merged_rentals[['season_name', '2011', '2012', 'percentage']])

st.subheader('Estimasi Kenaikan Penyewa pada tahun 2013')

# Plot the bike rentals including the estimation for 2013
plt.figure(figsize=(10, 6))
sns.barplot(x='season_name', y='2013_estimation', data=rentals_pivot, color='#5ce65c', label='2013 (Estimation)')
sns.barplot(x='season_name', y=2012, data=rentals_pivot, color='#e28743', label='2012')
sns.barplot(x='season_name', y=2011, data=rentals_pivot, color='#1e81b0', label='2011')

plt.title('Estimasi Penyewaan Sepeda untuk 2013 (Dengan 10% Kenaikan)')
plt.xlabel('Musim')
plt.ylabel('Jumlah Penyewaan')
plt.legend(title='Tahun')
plt.show()
st.pyplot(plt)

# Display the estimated rentals for 2013
st.subheader('Presentase Kenaikan Berdasarkan Musim')
st.table(rentals_pivot[['season_name', 2011, 2012, 'percentage_change', '2013_estimation']])

st.markdown("""
### Kesimpulan:
- Musim Dingin:
Peningkatan sebesar 58.06% dari 326.137 penyewaan pada 2011 menjadi 515.476 pada 2012 dengan Estimasi penyewaan untuk 2013 adalah 567.023.
    - Analisis: Meskipun musim dingin umumnya memiliki permintaan yang lebih rendah, peningkatan signifikan ini menunjukkan adanya potensi pertumbuhan lebih lanjut.
- Musim Gugur:
Peningkatan sebesar 52.86% dari 419.650 penyewaan pada 2011 menjadi 641.479 pada 2012 dengan Estimasi penyewaan untuk 2013 adalah 705.627.
    - Analisis: Musim gugur menunjukkan pertumbuhan yang stabil, dan popularitas penyewaan sepeda masih cukup tinggi.
- Musim Panas:
Peningkatan sebesar 64.48% dari 347.316 penyewaan pada 2011 menjadi 571.273 pada 2012 dengan Estimasi penyewaan untuk 2013 adalah 628.400.
    - Analisis: Musim panas memiliki pertumbuhan yang kuat karena cuaca yang optimal untuk bersepeda. Ini merupakan musim yang paling strategis untuk promosi.
- Musim Semi:
Peningkatan paling signifikan, yaitu 114.23%, dari 150.000 penyewaan pada 2011 menjadi 321.348 pada 2012 dengan Estimasi penyewaan untuk 2013 adalah 353.483.
    - Analisis: Musim semi menunjukkan peningkatan yang luar biasa. Ini bisa disebabkan oleh promosi musiman atau faktor lain yang mendorong minat pelanggan. 
### Strategy:
Rekomendasi Strategis:
- Optimalkan Promosi di Musim Semi dan Musim Panas:
    - Musim semi memiliki pertumbuhan terbesar, yang menandakan potensi besar untuk mendorong pertumbuhan lebih lanjut dengan promosi yang tepat.
    - Musim panas juga menunjukkan peningkatan yang kuat, dan karena ini musim yang paling nyaman untuk bersepeda, strategi pemasaran yang agresif seperti paket langganan jangka panjang atau diskon kelompok bisa diterapkan.

- Tingkatkan Aktivitas di Musim Dingin:
    - Meski musim dingin biasanya kurang diminati, peningkatan 58% dari 2011 ke 2012 menunjukkan ada permintaan yang terus tumbuh.
    - Penawaran promosi seperti diskon besar atau perlengkapan gratis (misalnya jaket atau sarung tangan untuk pelanggan) bisa menjadi insentif untuk meningkatkan minat bersepeda di musim dingin.

- Fokus Pada Peningkatan Infrastruktur dan Pengalaman Pengguna:
    - Menambah stasiun sepeda di dekat tempat wisata populer atau area bisnis di musim semi dan musim panas bisa meningkatkan penyewaan.
    - Meningkatkan pengalaman pengguna dengan aplikasi pemantauan cuaca dan rute yang lebih baik juga bisa menarik lebih banyak pelanggan.

- Estimasi Peningkatan untuk 2013:
    - Menggunakan data pertumbuhan dari 2011 ke 2012 sebagai dasar, estimasi untuk tahun 2013 menunjukkan pertumbuhan stabil di semua musim. Mengembangkan rencana pemasaran yang terfokus di setiap musim akan memastikan tren pertumbuhan ini terus berlanjut.""")




# Menampilkan plot di Streamlit
st.title('Pola penyewaan sepeda')


plt.figure(figsize=(10, 6))
sns.barplot(data=summary, x='workingday', y='cnt', palette='viridis')
plt.title('Pola Penyewaan Sepeda di Hari Kerja vs Akhir Pekan/Hari Libur')
plt.xlabel('Jenis Hari')
plt.ylabel('Jumlah Penyewaan Sepeda')
for index, row in summary.iterrows():
    plt.text(index, row['cnt'], f'{row["cnt"]}', color='black', ha="center")

plt.show()
st.pyplot(plt)

st.title("Perbandingan Penggunaan Sepeda antara Hari Kerja dan Hari Libur")
# Membuat dua kolom
col1, col2 = st.columns(2)

# Menampilkan informasi dalam kolom
with col1:
    st.metric(label="Total Penyewaan di Hari Kerja", value=total_workingday)
    st.metric(label="Total Penyewaan di Hari Libur", value=total_holiday)

with col2:
    st.metric(label="Persentase Perbedaan", value=f"{percentage_difference:.2f}%", delta=f"{percentage_difference:.2f}%")
st.markdown("""
### Kesimpulan 2 :
Dari analisis yang dilakukan, diperoleh informasi mengenai rata-rata jumlah penyewaan sepeda per hari pada hari kerja dan akhir pekan/hari libur selama tahun 2011-2012. Hasilnya menunjukkan bahwa:

- Rata-rata Penyewaan di Hari Kerja: Penyewaan sepeda cenderung lebih tinggi pada hari kerja dibandingkan dengan akhir pekan atau hari libur. Hal ini mungkin disebabkan oleh penggunaan sepeda sebagai moda transportasi sehari-hari bagi pekerja.
- Rata-rata Penyewaan di Akhir Pekan/Hari Libur: Meskipun jumlah penyewa di akhir pekan atau hari libur lebih rendah, tren ini menunjukkan potensi untuk meningkatkan penggunaan sepeda di waktu-waktu tersebut.### Strategi:
- Promosi Khusus untuk Akhir Pekan/Hari Libur:
 Buat promosi atau diskon khusus untuk penyewaan sepeda di akhir pekan atau hari libur untuk menarik lebih banyak pengguna. Misalnya, tawarkan diskon 20% untuk penyewaan di akhir pekan atau paket keluarga.

- Kampanye Pemasaran yang Menarik:
Luncurkan kampanye pemasaran yang berfokus pada manfaat kesehatan dan lingkungan dari bersepeda, terutama selama akhir pekan. Gunakan media sosial, influencer, dan komunitas lokal untuk meningkatkan kesadaran.
""")
