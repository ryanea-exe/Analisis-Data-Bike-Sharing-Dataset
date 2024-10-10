# Import library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def count_hour_df(bs_hour_df):
  bs_hour_df_count =  bs_hour_df.groupby(by="hour").agg({"count": ["sum"]})
  return bs_hour_df_count

def count_day_df(bs_day_df):
    bs_day_df_count = bs_day_df.groupby('day', observed=True)['count'].sum().reset_index()
    return bs_day_df_count

def count_day_type_df(bs_day_df):
    bs_day_type_df_count = bs_day_df.groupby('day_type', observed=True)['count'].sum().reset_index()
    return bs_day_type_df_count

def count_month_df(bs_day_df):
    bs_day_df['month'] = bs_day_df['date'].dt.to_period('M')
    bs_month_df_count = bs_day_df.groupby('month')['count'].sum().reset_index()
    return bs_month_df_count

def sum_order_df (bs_hour_df):
    order_df_sum = bs_hour_df.groupby("hour")['count'].sum().sort_values(ascending=False).reset_index()
    return order_df_sum

def sum_registered_df(bs_day_df):
   registered_df_sum =  bs_day_df.groupby(by="date").agg({
      "registered": "sum"
    })
   registered_df_sum = registered_df_sum.reset_index()
   registered_df_sum.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return registered_df_sum

def sum_casual_df(bs_day_df):
   casual_df_sum =  bs_day_df.groupby(by="date").agg({
      "casual": ["sum"]
    })
   casual_df_sum = casual_df_sum.reset_index()
   casual_df_sum.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return casual_df_sum

def sum_season (bs_day_df): 
    season_df_sum = bs_day_df.groupby(by="season")['count'].sum().reset_index() 
    return season_df_sum

# Load dataset
bs_days_df = pd.read_csv("dashboard/bs_day_df.csv")
bs_hours_df = pd.read_csv("dashboard/bs_hour_df.csv")

# Konversi kolom 'date' ke tipe datetim
datetime_columns = ["date"]
bs_days_df.sort_values(by="date", inplace=True)
bs_days_df.reset_index(inplace=True)   

bs_hours_df.sort_values(by="date", inplace=True)
bs_hours_df.reset_index(inplace=True)

for column in datetime_columns:
    bs_days_df[column] = pd.to_datetime(bs_days_df[column])
    bs_hours_df[column] = pd.to_datetime(bs_hours_df[column])

min_date_days = bs_days_df["date"].min()
max_date_days = bs_days_df["date"].max()

min_date_hour = bs_hours_df["date"].min()
max_date_hour = bs_hours_df["date"].max()

# Halaman Sidebar
with st.sidebar:
    # Logo perusahaan
    st.image("https://static.vecteezy.com/system/resources/previews/005/089/277/non_2x/inspiration-logo-mountain-bike-cycling-mtb-isolated-silhouette-vector.jpg")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_bs_days_df = bs_days_df[(bs_days_df["date"] >= str(start_date)) & 
                       (bs_days_df["date"] <= str(end_date))]

main_bs_hours_df = bs_hours_df[(bs_hours_df["date"] >= str(start_date)) & 
                        (bs_hours_df["date"] <= str(end_date))]

# Menghitung data berdasarkan filter
bs_hour_df_count = count_hour_df(main_bs_hours_df)
bs_day_df_count = count_day_df(main_bs_days_df)
bs_day_type_df_count = count_day_type_df(main_bs_days_df)
bs_month_df_count = count_month_df(main_bs_days_df)
registered_df_sum = sum_registered_df(main_bs_days_df)
casual_df_sum = sum_casual_df(main_bs_days_df)
order_df_sum = sum_order_df(main_bs_hours_df)
season_df_sum = sum_season(main_bs_days_df)

# Halaman Dashboard dengan Berbagai Data Visualization
st.header('Bike Sharing Dataset :sparkles:')

# Halaman daily bike sharing
st.subheader('Daily Bike Sharing')
col1, col2, col3 = st.columns(3)

with col1:
    sum_order = bs_day_df_count['count'].sum()
    st.metric("Jumlah Total Pengguna Sepeda", value=sum_order)

with col2:
    sum_registered = registered_df_sum.register_sum.sum()
    st.metric("Jumlah Pengguna Sepeda 'Registered'", value=sum_registered)

with col3:
    sum_casual = casual_df_sum.casual_sum.sum()
    st.metric("Jumlah Pengguna Sepeda 'Casual'", value=sum_casual)

# Halaman perbedaan jumlah pengguna sepeda antara weekday dan weekend
st.subheader("Perbedaan jumlah pengguna sepeda antara weekday dan weekend")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Palet warna yang sesuai dengan jumlah data
colors_day = ["#728FCE", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#728FCE"]
colors_day_type = ["#D3D3D3", "#728FCE"]

sns.barplot(x="count", y="day", data=bs_day_df_count.head(7), palette=colors_day, hue="day", legend=False, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Jumlah pengguna per Day", loc="center", fontsize=42)
ax[0].set_xlabel('(Jumlah)', fontsize=28)
ax[0].set_ylabel('(Day)', fontsize=28)
ax[0].tick_params(axis='y', labelsize=24)
ax[0].tick_params(axis='x', labelsize=24)
 
sns.barplot(x="count", y="day_type", data=bs_day_type_df_count.head(2), palette=colors_day_type, hue="day_type", legend=False, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Jam pengguna per Day Type", loc="center", fontsize=42)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_xlabel('(Jumlah)', fontsize=28)
ax[1].set_ylabel('(Day Type)', fontsize=28)
ax[1].tick_params(axis='y', labelsize=24)
ax[1].tick_params(axis='x', labelsize=24) 

st.pyplot(fig)

# Halaman performa penggunaan sepeda per bulan dalam 1 tahun terakhir
st.subheader("Performa penggunaan sepeda per bulan dalam 1 tahun terakhir")
fig, ax = plt.subplots(figsize=(24, 8))

# Menghitung jumlah pelanggan maksimum per bulan, untuk 1 tahun terakhir
last_year_data = main_bs_days_df[main_bs_days_df['date'] >= (main_bs_days_df['date'].max() - pd.DateOffset(years=1))]
month_count = last_year_data.resample('M', on='date')['count'].sum().reset_index()

ax.scatter(month_count['date'], month_count['count'], c="#90CAF9", s=100, marker='o')
ax.plot(month_count['date'], month_count['count'], color='blue',)
ax.set_xticks(month_count['date'])
ax.set_xticklabels(month_count['date'].dt.strftime('%B'), rotation=45, fontsize=16)
ax.set_xlabel('(Bulan (Tahun 2012))', fontsize=20)
ax.set_ylabel('(Jumlah)', fontsize=20)
ax.set_title('Grafik Jumlah Pelanggan per Bulan dalam 1 Tahun Terakhir', fontsize=32)

plt.tight_layout()
st.pyplot(fig)

# Halaman perbandingan pengaruh musim terhadap jumlah pengguna sepeda
st.subheader("Perbandingan pengaruh musim terhadap jumlah pengguna sepeda")

season_count = main_bs_days_df.groupby('season', observed=True)['count'].sum().reset_index()

data = season_count['count'].values
labels = season_count['season'].astype(str)
col1, col2 = st.columns([2, 1])

with col1:
    # Membuat pie plot dengan persentase
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(data, labels=labels, autopct='%1.1f%%', colors=["#D3D3D3", "#72BCD4", "#FFD700", "#FF6347"])
    ax.set_title('Persentase Jumlah Pengguna Berdasarkan Season')

    st.pyplot(fig)

with col2:
    # Menambahkan tabel di sebelah kanan pie chart dengan Streamlit
    st.write("Tabel Jumlah Pengguna Berdasarkan Season:")
    st.table(season_count)
