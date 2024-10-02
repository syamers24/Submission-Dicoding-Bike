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

st.markdown("""
### Kesimpulan:
Berdasarkan plot diatas kita mengetahui bahwa Bike Sharing mengalami peningkatan yang signifikan selama satu tahun dan peningkatan terbesar nya terjadi di musim semi, disini kita tahu bahwa musim gugur mengalami kenaikan yang paling rendah,
dari hal itu kita mengetahui bahwa kita memerlukan sesuatu untuk menaikan Penyewaan pada Musim gugur 
### Strategy:
Mengadakan discount atau promosi yang terfokus pada musim tersebut sehingga dapat menaikan Penyewaan nya.
""")




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
- Kesimpulan dari Visual diatas, Banyak pengguna menyewa sepeda untuk keperluan sehari-hari, seperti perjalanan ke tempat kerja, sekolah, atau aktivitas lain yang berkaitan dengan rutinitas harian mereka, 
Penurunan jumlah penyewa di hari libur menunjukkan bahwa penggunaan sepeda untuk kegiatan rekreasi atau hobi mungkin masih rendah.
 Ini bisa jadi karena faktor kurangnya promosi untuk penggunaan sepeda di akhir pekan, atau adanya alternatif transportasi lainnya. 
### Strategi:
- Meningkatkan lagi promosi yang secara spesifik pada hari libur sehingga dapat menaikan pengguna atau penyewa di hari libur atau akhir pekan, Misalnya, tawarkan diskon atau paket khusus untuk penyewaan sepeda di akhir pekan.
""")
