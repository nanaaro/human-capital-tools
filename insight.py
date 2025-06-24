import streamlit as st
import os

def show():
    st.title("🔍 Fitur Evaluasi Human Capital")

    fitur_dict = {
        "Environment Satisfaction": "Tingkat kepuasan terhadap lingkungan kerja secara umum. Lingkungan yang nyaman mendukung produktivitas, sementara lingkungan buruk bisa menurunkan performa.",
        "Job Satisfaction": "Kepuasan terhadap pekerjaan dan peran saat ini. Pegawai yang puas biasanya lebih termotivasi dan menunjukkan kinerja tinggi.",
        "Relationship Satisfaction": "Kepuasan terhadap hubungan dengan rekan kerja atau atasan. Hubungan kerja yang sehat mendorong kolaborasi dan efisiensi.",
        "Training Opportunities Within Year": "Kesempatan pelatihan yang tersedia dalam setahun. Menunjukkan dukungan perusahaan terhadap pengembangan karier.",
        "Training Opportunities Taken": "Jumlah pelatihan yang diikuti. Menunjukkan inisiatif dan motivasi untuk berkembang.",
        "Work Life Balance": "Keseimbangan antara pekerjaan dan kehidupan pribadi. Ketidakseimbangan bisa menyebabkan burnout dan berdampak pada performa.",
        "Business Travel": "Frekuensi perjalanan dinas. Sering bepergian bisa menunjukkan tanggung jawab tinggi atau menambah beban kerja.",
        "OverTime": "Kebiasaan bekerja lembur. Bisa mencerminkan dedikasi atau overwork, yang keduanya berdampak berbeda tergantung konteks.",
        "Years At Company": "Lama pegawai bekerja di perusahaan. Bisa menjadi indikator loyalitas atau stagnasi jika tidak dibarengi perkembangan.",
        "Years In Most Recent Role": "Durasi berada di posisi terakhir. Terlalu lama di satu peran bisa menandakan kurangnya mobilitas atau pengembangan.",
        "Years Since Last Promotion": "Lama sejak promosi terakhir. Semakin lama tanpa promosi bisa membuat pegawai merasa kurang diapresiasi.",
        "Years With Current Manager": "Durasi bekerja dengan manajer saat ini. Hubungan jangka panjang bisa menjadi tanda stabilitas atau stagnasi.",
        "Promotion Ratio": "Proporsi durasi peran terakhir terhadap total masa kerja. Nilai tinggi bisa mengindikasikan pegawai stagnan di satu posisi.",
        "Stagnancy Score": "Perbandingan waktu sejak promosi terakhir dengan total masa kerja. Skor tinggi menunjukkan minimnya perkembangan karier.",
        "Manager Stability": "Stabilitas hubungan dengan atasan, dilihat dari lamanya bekerja bersama. Stabilitas ini bisa membantu atau menghambat kemajuan tergantung dinamika hubungan.",
        "Manager Rating": "Nilai penilaian dari manajer terhadap performa. Dijadikan variabel target: rating 1–2 berarti perlu evaluasi, sedangkan 3–5 berarti memenuhi ekspektasi."
    }

    pilihan = st.selectbox("📌 Pilih fitur untuk melihat penjelasan:", list(fitur_dict.keys()))
    st.markdown(f"""
        <div style='margin-bottom: 10px;'>
            <h4 style='color: #1f77b4; font-size: 17px;'>{pilihan}</h4>
            <p style='font-size: 13px; color: #444; margin: 0;'>{fitur_dict[pilihan]}</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Insight Visualisasi EDA")

    eda_figures = [
        {
            "judul": "Years Since Last Promotion vs Manager Rating",
            "file": "HC/Figure_1.png",
            "deskripsi": """
            Rata-rata waktu sejak promosi terakhir pada tiap kategori ManagerRating tidak menunjukkan penurunan yang konsisten. 
            Rating 2 memiliki rata-rata 4.10 tahun, naik ke 4.22 tahun pada rating 3, dan 4.36 tahun pada rating 4, lalu justru sedikit turun menjadi 4.26 tahun pada rating 5. 
            Pola ini menunjukkan bahwa fitur YearsSinceLastPromotion tidak secara langsung merepresentasikan performa yang menurun. 
            Meski demikian, fitur ini tetap relevan dalam menilai stagnansi karier apabila digunakan bersama indikator turunan lain seperti promotion_ratio dan stagnancy_score.
            """
        },
        {
            "judul": "Promotion Ratio vs Manager Rating",
            "file": "HC/Figure_2.png",
            "deskripsi": """
            Rata-rata promotion_ratio cenderung meningkat seiring dengan naiknya ManagerRating. 
            Pegawai dengan rating 2 dan 3 memiliki promotion_ratio sekitar 0.41, kemudian meningkat menjadi 0.43 pada rating 4, dan mencapai 0.44 pada rating 5. 
            Hal ini menunjukkan bahwa pegawai yang memiliki proporsi masa kerja yang lebih besar di posisi terakhir terhadap total masa kerja cenderung mendapatkan penilaian lebih baik dari manajer. 
            Dengan demikian, promotion_ratio dapat digunakan sebagai indikator penting dalam mengukur dinamika karier dan perkembangan profesional pegawai.
            """
        },
        {
            "judul": "Stagnancy Score vs Manager Rating",
            "file": "HC/Figure_3.png",
            "deskripsi": """
            Rata-rata stagnancy_score menunjukkan tren kenaikan dari rating 2 hingga rating 5, yaitu dari 0.619 ke 0.643. 
            Artinya, secara rata-rata, pegawai dengan rating tinggi justru memiliki nilai stagnancy_score yang juga tinggi. 
            Hal ini sedikit berbeda dari dugaan awal bahwa stagnansi karier (ditandai dengan lamanya sejak promosi terakhir dibanding total masa kerja) selalu berkonotasi negatif. 
            Temuan ini menunjukkan bahwa stagnancy_score perlu dilihat secara kontekstual, misalnya, beberapa pegawai tetap mendapatkan penilaian baik meski belum dipromosikan karena mungkin mereka memang telah berada pada posisi strategis atau tidak tersedia jalur promosi. 
            Maka, fitur stagnancy_score tetap relevan, namun interpretasinya harus disesuaikan dengan peran dan konteks struktural pegawai.
            """
        },
        {
            "judul": "OverTime vs Manager Rating",
            "file": "HC/Figure_4.png",
            "deskripsi": """
            Pegawai yang tidak lembur (OverTime = No) cenderung mendapat ManagerRating lebih tinggi. 
            Misalnya, pada rating 4 terdapat 1.463 pegawai yang tidak lembur dibanding 757 yang lembur. 
            Pola serupa terlihat di rating 5 dengan rasio 747:327. 
            Ini menunjukkan bahwa terlalu sering lembur bisa berdampak negatif terhadap penilaian, kemungkinan akibat kelelahan atau kurang efisiensi. 
            Oleh karena itu, fitur OverTime relevan sebagai indikator keseimbangan kerja.
            """
        },
        {
            "judul": "Business Travel vs Manager Rating",
            "file": "HC/Figure_5.png",
            "deskripsi": """
            Pegawai dengan frekuensi perjalanan dinas sedang (Some Travel) mendominasi rating tinggi. 
            Misalnya, pada rating 4 terdapat 1.560 pegawai yang melakukan Some Travel, dibanding hanya 447 Frequent Traveller dan 213 No Travel. 
            Pola serupa terlihat pada rating 5 (762 Some Travel vs 215 Frequent dan 97 No Travel). Ini menunjukkan bahwa eksposur kerja lapangan yang seimbang berkorelasi positif terhadap penilaian manajer. 
            Maka, fitur BusinessTravel penting untuk menangkap dinamika peran pegawai.
            """
        },
        {
            "judul": "Years in Current Role vs Manager Rating",
            "file": "HC/Figure_6.png",
            "deskripsi": """
            Rata-rata lama berada di peran terakhir cenderung meningkat seiring naiknya ManagerRating. 
            Pada rating 2 rata-ratanya 2.73 tahun, sementara pada rating 4 naik menjadi 2.99 tahun. 
            Meski terjadi sedikit penurunan pada rating 5 (2.92 tahun), secara umum terlihat bahwa durasi yang moderat dalam suatu peran berkontribusi terhadap performa yang lebih baik. 
            Oleh karena itu, fitur YearsInMostRecentRole tetap relevan untuk menilai pengalaman fungsional pegawai.
            """
        },
        {
            "judul": "Manager Stability vs Manager Rating",
            "file": "HC/Figure_7.png",
            "deskripsi": """
            Rata-rata nilai manager_stability relatif stabil di semua level rating, berkisar antara 0.41 hingga 0.43. 
            Nilai tertinggi muncul pada rating 5 (0.429), menunjukkan bahwa pegawai dengan hubungan jangka panjang dan stabil dengan manajernya cenderung memperoleh penilaian performa terbaik. 
            Ini memperkuat alasan dipertahankannya fitur manager_stability sebagai sinyal potensi dukungan atau kepercayaan manajerial.
            """
        },
        {
            "judul": "Korelasi Antar Fitur Numerik",
            "file": "HC/Figure_8.png",
            "deskripsi": """
            Korelasi antar fitur numerik menunjukkan hubungan yang lemah terhadap ManagerRating, dengan nilai tertinggi pada YearsInMostRecentRole (0.032), promotion_ratio (0.030), dan stagnancy_score (0.022). 
            Meskipun tidak ada korelasi kuat secara linier, fitur-fitur ini tetap relevan karena distribusi visualnya pada boxplot menunjukkan perbedaan yang berarti antar level rating. 
            Hal ini menekankan pentingnya mempertimbangkan pola non-linear dan interaksi fitur dalam pemodelan.
            """
        }
    ]

    for fig in eda_figures:
        if os.path.exists(fig["file"]):
            with st.expander(fig["judul"]):
                st.image(fig["file"], width=600)
                st.markdown(
                    f"<p style='font-size:14px; color:#444;'>{fig['deskripsi'].strip()}</p>",
                    unsafe_allow_html=True
                )
        else:
            st.warning(f"Gambar tidak ditemukan: {fig['file']}")
