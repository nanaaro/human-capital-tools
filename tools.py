import streamlit as st
import joblib
import pandas as pd

def show():
    st.header("🛠️ Human Capital Evaluation Tools")

    # Load model dan preprocessed data
    model_bundle = joblib.load("employee model.pkl")
    model = model_bundle['model']
    scaler = model_bundle['scaler']
    features = model_bundle['features']
    df_proc = pd.read_csv("Preprocessed Employee.csv")

    # Load data mentah
    perf = pd.read_csv("PerformanceRating.csv")
    emp = pd.read_csv("Employee.csv")

    # Gunakan review terbaru dari setiap pegawai
    perf_latest = perf.sort_values("ReviewDate").drop_duplicates("EmployeeID", keep="last")
    raw_df = pd.merge(perf_latest, emp, on="EmployeeID", how="left")

    # Hitung fitur turunan
    raw_df["promotion_ratio"] = raw_df["YearsInMostRecentRole"] / (raw_df["YearsAtCompany"] + 1e-5)
    raw_df["stagnancy_score"] = raw_df["YearsSinceLastPromotion"] / (raw_df["YearsAtCompany"] + 1e-5)
    raw_df["manager_stability"] = raw_df["YearsWithCurrManager"] / (raw_df["YearsAtCompany"] + 1e-5)

    # Ambil daftar EmployeeID unik dari data mentah (raw)
    employee_ids = raw_df["EmployeeID"].dropna().unique().tolist()
    employee_id = st.selectbox("Masukkan Employee ID", employee_ids)


    if not employee_id:
        st.info("Silakan masukkan Employee ID untuk melihat evaluasi.")
        return

    emp_data = df_proc[df_proc["EmployeeID"] == employee_id]
    raw_emp_data = raw_df[raw_df["EmployeeID"] == employee_id]

    if emp_data.empty or raw_emp_data.empty:
        st.error("Employee ID tidak ditemukan.")
        return

    st.success(f"Data ditemukan untuk ID {employee_id}")

    input_data = emp_data[features].copy()

    # Prediksi awal (tanpa simulasi)
    input_scaled = scaler.transform(input_data)
    importances = model.feature_importances_
    contrib = pd.Series(input_scaled[0] * importances, index=features).sort_values(ascending=False)
    top_features = contrib.head(7).index.tolist()

    # Prediksi hasil akhir
    pred = model.predict(input_scaled)[0]
    label = "Needs Improvement" if pred == 0 else "Meets Expectation"
    color = "red" if pred == 0 else "green"

    st.markdown(f"<h3 style='color:{color}'>Hasil Evaluasi: {label}</h3>", unsafe_allow_html=True)

    # Faktor yang Memengaruhi Evaluasi
    st.subheader("Faktor yang Memengaruhi Evaluasi")

    feature_name_map = {
        "EnvironmentSatisfaction": "Environment Satisfaction",
        "JobSatisfaction": "Job Satisfaction",
        "RelationshipSatisfaction": "Relationship Satisfaction",
        "TrainingOpportunitiesWithinYear": "Training Opportunities (Year)",
        "TrainingOpportunitiesTaken": "Total Training Taken",
        "WorkLifeBalance": "Work-Life Balance",
        "BusinessTravel": "Business Travel Frequency",
        "OverTime": "Overtime",
        "YearsAtCompany": "Years at Company",
        "YearsInMostRecentRole": "Years in Current Role",
        "YearsSinceLastPromotion": "Years Since Last Promotion",
        "YearsWithCurrManager": "Years with Current Manager",
        "promotion_ratio": "Promotion Ratio",
        "stagnancy_score": "Stagnancy Score",
        "manager_stability": "Manager Stability"
    }

    def tampilkan_nilai(fitur, nilai):
        # Fungsi untuk menampilkan nilai dengan format yang sesuai
        if fitur in ["OverTime"]:
            return "Ya" if str(nilai).lower() in ["1", "yes", "ya", "true"] else "Tidak"
        elif fitur in ["BusinessTravel"]:
            return str(nilai)
        elif fitur in ["WorkLifeBalance", "EnvironmentSatisfaction", "JobSatisfaction", "RelationshipSatisfaction"]:
            return int(float(nilai))
        elif "score" in fitur or "ratio" in fitur:
            return round(float(nilai), 2)
        else:
            return nilai

    nilai_asli = []
    for f in top_features:
        if f in raw_emp_data.columns:
            nilai_asli.append(tampilkan_nilai(f, raw_emp_data[f].values[0]))
        elif f in input_data.columns:
            nilai_asli.append(tampilkan_nilai(f, input_data[f].values[0]))
        else:
            nilai_asli.append("-")

    result_df = pd.DataFrame({
        "Fitur": [feature_name_map.get(f, f) for f in top_features],
        "Nilai Pegawai": nilai_asli,
        "Impact Score": contrib.loc[top_features].values
    })

    st.dataframe(result_df.style.format({"Impact Score": "{:.2f}"}), use_container_width=True)

    # Insight Evaluasi Otomatis
    st.markdown("### 🔍 Insight Evaluasi Otomatis")

    narrative = []
    raw = raw_emp_data.iloc[0]

    def is_low(val): return val <= 2
    def is_very_low(val): return val <= 1
    def is_high(val): return val >= 4
    def is_stagnant(val): return val >= 3
    def is_long(val): return val >= 5
    def is_new(val): return val <= 1

    if any(f in top_features for f in ["EnvironmentSatisfaction", "JobSatisfaction", "RelationshipSatisfaction"]):
        if any(is_low(raw[f]) for f in ["EnvironmentSatisfaction", "JobSatisfaction", "RelationshipSatisfaction"]):
            narrative.append("Nilai kepuasan kerja karyawan relatif rendah, baik dari sisi lingkungan kerja, peran, maupun hubungan antar rekan.")

    if any(f in top_features for f in ["YearsInMostRecentRole", "YearsSinceLastPromotion", "promotion_ratio", "stagnancy_score"]):
        if is_stagnant(raw["YearsInMostRecentRole"]) and is_stagnant(raw["YearsSinceLastPromotion"]):
            narrative.append("Terdapat indikasi stagnansi karena karyawan telah cukup lama dalam posisi yang sama tanpa promosi.")
        elif is_new(raw["YearsInMostRecentRole"]) or is_new(raw["YearsSinceLastPromotion"]):
            narrative.append("Karyawan masih dalam masa adaptasi terhadap peran atau belum lama sejak promosi terakhir.")

    if raw["TrainingOpportunitiesWithinYear"] == 0 or raw["TrainingOpportunitiesTaken"] == 0:
        narrative.append("Minimnya kesempatan atau partisipasi dalam pelatihan menjadi salah satu penyebab stagnansi.")

    if any(f in top_features for f in ["WorkLifeBalance", "BusinessTravel", "OverTime"]):
        overtime = str(raw["OverTime"]).lower()
        travel = str(raw["BusinessTravel"]).lower()
        if is_low(raw["WorkLifeBalance"]) or overtime in ["yes", "1"] or "frequent" in travel:
            narrative.append("Terdapat tekanan beban kerja yang cukup tinggi, baik dari sisi lembur, perjalanan dinas, maupun keseimbangan kerja dan kehidupan pribadi.")

    if "YearsWithCurrManager" in top_features or "manager_stability" in top_features:
        if is_new(raw["YearsWithCurrManager"]):
            narrative.append("Karyawan masih dalam tahap adaptasi dengan manajer barunya.")
        elif is_long(raw["YearsWithCurrManager"]):
            narrative.append("Hubungan kerja yang terlalu lama tanpa dinamika baru dapat menjadi faktor penurunan performa.")

    if narrative:
        for i, para in enumerate(narrative, 1):
            st.markdown(f"**{i}.** {para}")
    else:
        st.info("Tidak ada insight spesifik yang dapat disimpulkan dari kombinasi fitur saat ini.")

    # 🔧 Simulasi Evaluasi (dipindahkan ke dalam fungsi)
    with st.expander("⚙️ Simulasi Evaluasi (Opsional)"):
        simulate = st.checkbox("Aktifkan Simulasi Manual", key="Aktifkan Simulasi Manual")

        if simulate:
            st.markdown("Ubah beberapa faktor berikut untuk mensimulasikan dampaknya terhadap hasil evaluasi karyawan.")

            for f in top_features:
                if f not in input_data.columns:
                    continue

                if f in raw_emp_data.columns:
                    curr_val = raw_emp_data[f].values[0]
                else:
                    curr_val = input_data[f].values[0]

                label = feature_name_map.get(f, f)

                if f == "OverTime":
                    selected = st.selectbox(
                        "Lembur?",
                        options=["Tidak", "Ya"],
                        index=1 if str(curr_val).lower() in ["1", "yes", "ya", "true"] else 0
                    )
                    input_data[f] = 1 if selected.lower() == "ya" else 0

                elif f == "BusinessTravel":
                    travel_options = ["No Travel", "Some Travel", "Frequent Travel"]
                    selected = st.selectbox(
                        "Frekuensi Perjalanan Dinas",
                        options=travel_options,
                        index=travel_options.index(curr_val) if curr_val in travel_options else 0
                    )
                    input_data[f] = selected

                elif f == "WorkLifeBalance":
                    selected = st.selectbox(
                        "Work-Life Balance",
                        options=["Rendah (1)", "Sedang (2)", "Baik (3)", "Sangat Baik (4)"],
                        index=int(curr_val)-1 if int(curr_val) in [1, 2, 3, 4] else 2
                    )
                    input_data[f] = int(selected[-2])

                elif f in ["EnvironmentSatisfaction", "JobSatisfaction", "RelationshipSatisfaction"]:
                    input_data[f] = st.slider(label, 1, 5, int(curr_val))

                elif f in ["TrainingOpportunitiesWithinYear", "TrainingOpportunitiesTaken"]:
                    input_data[f] = st.slider(label, 0, 10, int(curr_val))

                elif "score" in f or "ratio" in f:
                    input_data[f] = st.slider(label, 0.0, 5.0, float(curr_val), step=0.1)

            # Evaluasi hasil setelah simulasi
            st.markdown("---")
            st.subheader("📝 Hasil Evaluasi Setelah Simulasi")

            input_scaled_sim = scaler.transform(input_data)
            pred_sim = model.predict(input_scaled_sim)[0]
            label_sim = "Needs Improvement" if pred_sim == 0 else "Meets Expectation"
            color_sim = "red" if pred_sim == 0 else "green"

            st.markdown(f"<h4 style='color:{color_sim}'>Simulasi Evaluasi: {label_sim}</h4>", unsafe_allow_html=True)
