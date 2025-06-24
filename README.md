# Human Capital Evaluation

## Tujuan

- Menyediakan insight eksploratif (EDA) berbasis data terhadap faktor-faktor yang memengaruhi penilaian manajer.
- Membantu dalam pemilihan fitur penting untuk model prediksi evaluasi kinerja.
- Menyajikan data dalam bentuk grafik, ringkasan numerik, dan interpretasi singkat secara interaktif.

## Dataset

Sistem ini menggunakan dua dataset utama:

- `Employee.csv` — Berisi informasi demografi dan pekerjaan karyawan.
- `PerformanceRating.csv` — Berisi hasil penilaian manajer terhadap kinerja karyawan.

Data digabung berdasarkan `EmployeeID`.

## Fitur Visualisasi

Beberapa fitur yang dianalisis dan divisualisasikan:

- YearsSinceLastPromotion
- Promotion Ratio (fitur turunan)
- Stagnancy Score (fitur turunan)
- OverTime
- Business Travel
- YearsInMostRecentRole
- Manager Stability (fitur turunan)
- Korelasi antar fitur numerik

Setiap visualisasi dilengkapi dengan interpretasi kuantitatif dan insight pengambilan keputusan.

## Cara Menjalankan Sistem

1. Clone repository ini:

```bash
git clone https://github.com/username/hc-streamlit.git
cd hc-streamlit
````

2. Instal dependencies:

```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:

```bash
streamlit run app.py
```

## 🌐 Hosting Online

Aplikasi ini bisa dijalankan secara gratis melalui [Streamlit Community Cloud](https://streamlit.io/cloud).

## 📁 Struktur Folder

```
hc-streamlit/
│
├── app.py                  # File utama Streamlit
├── requirements.txt        # Daftar dependensi Python
├── data/
│   ├── Employee.csv
│   └── PerformanceRating.csv
├── eda_figures/
│   ├── Figure_1.png
│   ├── ...
└── README.md
```

## Library yang Digunakan

* Python
* Streamlit
* Pandas
* Seaborn & Matplotlib
* scikit-learn

